from logging import Logger
import os
from typing import Callable, Iterable, List, Any

import fire
from torch.cuda.amp import autocast, GradScaler
from torch.utils.tensorboard import SummaryWriter
import torch
from torch.nn import functional as F
from random import shuffle


from easy_vc_dev.commons import clip_grad_value_, slice_segments
from easy_vc_dev.const import TRAINER_DIR

from easy_vc_dev.misc.HParams import get_LightweightRVC_Synthesizer_nof0_hparams
from easy_vc_dev.train.save_checkpoint import save_checkpoints
from easy_vc_dev.train.generate_data_loader import generate_data_loader
from easy_vc_dev.train.generate_gpu_cache import generate_gpu_cache
from easy_vc_dev.train.generate_train_components import generate_train_components
from easy_vc_dev.train.load_checkpoints import load_checkpoints
from easy_vc_dev.train.losses import discriminator_loss, feature_loss, generator_loss, kl_loss
from easy_vc_dev.train.tensorboard_utils.summarize import summarize
from easy_vc_dev.utils.get_logger import get_logger
from easy_vc_dev.utils.mel_processing import mel_spectrogram_torch, spec_to_mel_torch
from easy_vc_dev.utils.parseBoolArg import parseBoolArg
from easy_vc_dev.train.tensorboard_utils.plot_spectrogram_to_numpy import plot_2spectrogram_to_numpy

MEL_LOSS_RATIO = 1
KL_LOSS_RATIO = 1


def print_training_info(logger: Logger, iteration_per_epoch: int, batch_size: int, total_epochs: int, start_epoch: int, start_global_step: int):
    logger.info("**" * 40)
    logger.info(f"batch size: {batch_size}")
    logger.info(f"iterations per epoch: {iteration_per_epoch}")
    logger.info(f"total of epochs: {total_epochs}")
    logger.info(f"started at epoch: {start_epoch}")
    logger.info(f"started at global step: {start_global_step}")
    logger.info("**" * 40 + "\n")


def set_next_data(info, device_id: int, use_f0: bool, cache_gpu: bool):
    info_on_gpu = [x.cuda(device_id, non_blocking=True) for x in info]
    return info_on_gpu


def process_infer(
    generator,
    phone,
    phone_lengths,
    pitch,
    pitchf,
    spec,
    spec_lengths,
    filter_length,
    n_mel_channels,
    sampling_rate,
    hop_length,
    win_length,
    mel_fmin,
    mel_fmax,
    fp16_run,
):
    # ジェネレータでwaveformを推論
    with autocast(enabled=fp16_run):
        if pitch is not None:
            y_hat, ids_slice, x_mask, z_mask, (z, z_p, m_p, logs_p, m_q, logs_q) = generator(phone, phone_lengths, pitch, pitchf, spec, spec_lengths)
        else:
            y_hat, ids_slice, x_mask, z_mask, (z, z_p, m_p, logs_p, m_q, logs_q) = generator(phone, phone_lengths, spec, spec_lengths)

        # 生成したwavformをmelスペクトログラムに変換
        with autocast(enabled=False):
            y_hat_mel = mel_spectrogram_torch(
                y_hat.float().squeeze(1),
                filter_length,
                n_mel_channels,
                sampling_rate,
                hop_length,
                win_length,
                mel_fmin,
                mel_fmax,
            )
        if fp16_run is True:
            y_hat_mel = y_hat_mel.half()
    return ids_slice, y_hat, y_hat_mel, (z_p, logs_q, m_p, logs_p, z_mask)


def get_gt_data(
    wave,
    spec,
    ids_slice,
    segment_size,
    y_hat_size,
    y_hat_mel_size,
    filter_length,
    n_mel_channels,
    sampling_rate,
    hop_length,
    win_length,
    mel_fmin,
    mel_fmax,
    fp16_run,
):
    with autocast(enabled=fp16_run):
        # 正解のwevformをセグメント分切り出し
        if segment_size == y_hat_size:
            wave = slice_segments(wave, ids_slice * hop_length, segment_size)
        else:
            wave = slice_segments(wave, ids_slice * hop_length, y_hat_size)

        # 正解のメルスペクトログラムをメルスペクトログラムに変換してセグメント分切り出し
        mel = spec_to_mel_torch(
            spec,
            filter_length,
            n_mel_channels,
            sampling_rate,
            mel_fmin,
            mel_fmax,
        )
        # y_mel = slice_segments(mel, ids_slice, hps.train.segment_size // hps.data.hop_length)
        y_mel = slice_segments(mel, ids_slice, y_hat_mel_size)
    return wave, y_mel


def train_discriminator(
    discriminator,
    optimizer_discriminator,
    scaler,
    wave,
    y_hat,
    fp16_run,
):
    with autocast(enabled=fp16_run):
        y_d_hat_r, y_d_hat_g, _, _ = discriminator(wave, y_hat.detach())

        with autocast(enabled=False):
            loss_disc, _, _ = discriminator_loss(y_d_hat_r, y_d_hat_g)
        optimizer_discriminator.zero_grad()
        scaler.scale(loss_disc).backward()
        scaler.unscale_(optimizer_discriminator)
        grad_norm_d = clip_grad_value_(discriminator.parameters(), None)
        scaler.step(optimizer_discriminator)
    return grad_norm_d, loss_disc


def train_generator(
    generator,
    discriminator,
    optimizer_generator,
    scaler,
    wave,
    y_hat,
    loss_for_mel,
    loss_for_kl,
    mel_loss_factor,
    kl_loss_factor,
    fp16_run,
):
    (y_mel, y_hat_mel) = loss_for_mel
    (z_p, logs_q, m_p, logs_p, z_mask) = loss_for_kl
    with autocast(enabled=fp16_run):
        _, y_d_hat_g, fmap_r, fmap_g = discriminator(wave, y_hat)

        with autocast(enabled=False):
            # print(f"y_mel, y_hat_mel,{y_mel.shape},{y_hat_mel.shape}")
            # print(f"-------------------- - - - -2-- -  wav: {wave.shape}, y_hat:{y_hat.shape}")
            loss_mel = F.l1_loss(y_mel, y_hat_mel) * mel_loss_factor
            loss_kl = kl_loss(z_p, logs_q, m_p, logs_p, z_mask) * kl_loss_factor

            # print(f"fmap_r, fmap_g,{fmap_r[0][0].shape},{fmap_g[0][0].shape}")
            loss_fm = feature_loss(fmap_r, fmap_g)
            loss_gen, losses_gen = generator_loss(y_d_hat_g)
            loss_gen_all = loss_gen + loss_fm + loss_mel + loss_kl
        optimizer_generator.zero_grad()
        scaler.scale(loss_gen_all).backward()
        scaler.unscale_(optimizer_generator)
        grad_norm_g = clip_grad_value_(generator.parameters(), None)
        scaler.step(optimizer_generator)
        scaler.update()
    return grad_norm_g, loss_gen_all, loss_mel, loss_kl, loss_fm, loss_gen


def train(
    project_name: str,
    # config_path: str,
    sample_rate: int,
    use_f0: bool,
    total_epoch: int,
    batch_size: int,
    device_id: int,
    log_step_interval: int,
    val_step_interval: int,
    test_step_interval: int,
    save_model_epoch_interval: int,
    checkpoint_path: str | None = None,
    cache_gpu: bool = False,
    freeze_vocoder: bool = True,
    finetune: bool = False,
    vocoder_ckpt: str | None = None,
    callback: Callable[[str, int, int, str], None] | None = None,
):
    assert checkpoint_path is not None or vocoder_ckpt is not None, "specify checkpoint_path or vocoder_ckpt."

    use_f0 = parseBoolArg(use_f0)
    cache_gpu = parseBoolArg(cache_gpu)
    freeze_vocoder = parseBoolArg(freeze_vocoder)

    project_dir = os.path.join(TRAINER_DIR, project_name)
    log_dir = os.path.join(project_dir, "logs")

    # ハイパーパラメータの読み込み
    # hps = get_hparams(log_dir, config_path)
    hps = get_LightweightRVC_Synthesizer_nof0_hparams()

    # ログ設定
    logger = get_logger(log_dir)

    # TensorBoard設定
    writer = SummaryWriter(log_dir=log_dir)

    # トレーニング環境設定
    torch.manual_seed(hps.train.seed)  # type: ignore
    torch.cuda.set_device(device_id)

    # トレーニングのコンポーネントを生成
    (
        generator,
        discriminator,
        optimizer_generator,
        optimizer_discriminator,
        scheduler_generator,
        scheduler_discriminator,
    ) = generate_train_components(use_f0=False, hps=hps)

    # データローダーを生成
    (
        train_loader,
        val_loader,
        test_loader,
        train_sampler,
    ) = generate_data_loader(project_dir, use_f0, batch_size, hps)

    # ジェネレータとディスクリミネーターのロード。レジューム対応
    if checkpoint_path is not None:
        sample_rate, global_step, epoch, best_mel_loss = load_checkpoints(
            checkpoint_path,
            generator,
            discriminator,
            optimizer_generator,
            optimizer_discriminator,
            scheduler_generator,
            scheduler_discriminator,
            logger,
            finetune,
        )
    else:
        global_step, epoch, best_mel_loss = 0, 0, float("inf")

    if vocoder_ckpt is not None:
        generator.load_vocoder(vocoder_ckpt)

    scaler = GradScaler(enabled=hps.train.fp16_run)

    # Vocoderの重みを固定
    if freeze_vocoder:
        print("!!!! FREEZE VOCODER !!!!")
        generator.freeze_vocoder_weights()

    # パラメータの転送
    generator = generator.cuda(device_id)
    discriminator = discriminator.cuda(device_id)

    for state in optimizer_generator.state.values():
        for k, v in state.items():
            if torch.is_tensor(v):
                state[k] = v.cuda(device_id)
    for state in optimizer_discriminator.state.values():
        for k, v in state.items():
            if torch.is_tensor(v):
                state[k] = v.cuda(device_id)

    # GPUキャッシュ
    if cache_gpu:
        cache: List[Any] | None = generate_gpu_cache(use_f0, device_id, train_loader)
    else:
        cache = None

    # epoch数の計算
    n_epochs = total_epoch
    batch_size = batch_size
    if finetune:
        print(f"Finetuning. reset learning rate from {optimizer_generator.param_groups[0]['lr']} to {hps.train.learning_rate}")
        print(f"Finetuning. reset global step from {global_step} to 0.")
        global_step = 0
    start_epoch = global_step // len(train_loader) + 1
    iteration_per_epoch = len(train_loader)
    print_training_info(logger, iteration_per_epoch, batch_size, n_epochs, start_epoch, global_step)

    # print(f"inter_channels:{hps.model.inter_channels}, upsample_initial_channel:{hps.model.upsample_initial_channel}")
    best_mel_loss = float("inf")

    for epoch in range(start_epoch, n_epochs + 1):
        print(f"Epoch Start(Epoch:{epoch}, GlobalStep:{global_step})")

        train_sampler.set_epoch(epoch)
        generator.train()
        discriminator.train()
        progress_batch_index = 0

        # データローダーの初期化
        if cache is not None:
            shuffle(cache)
            data_iterator: Iterable[Any] = cache
        else:
            data_iterator = enumerate(train_loader)

        # ミニバッチ
        for i, (batch_idx, info) in enumerate(data_iterator, 1):
            if callback is not None:
                callback(f"epoch: {epoch:03d}/{n_epochs:03d}", progress_batch_index, iteration_per_epoch, "RUNNING")
            progress_batch_index += 1
            if use_f0:
                phone, phone_lengths, pitch, pitchf, spec, spec_lengths, wave, wave_lengths, sid = set_next_data(info, device_id, use_f0, cache_gpu)

            else:
                phone, phone_lengths, spec, spec_lengths, wave, wave_lengths, sid = set_next_data(info, device_id, use_f0, cache_gpu)
                pitch = pitchf = None

            # ジェネレータでwaveformを推論
            ids_slice, y_hat, y_hat_mel, (z_p, logs_q, m_p, logs_p, z_mask) = process_infer(
                generator,
                phone,
                phone_lengths,
                pitch,
                pitchf,
                spec,
                spec_lengths,
                hps.data.filter_length,
                hps.data.n_mel_channels,
                hps.data.sampling_rate,
                hps.data.hop_length,
                hps.data.win_length,
                hps.data.mel_fmin,
                hps.data.mel_fmax,
                hps.train.fp16_run,
            )
            # GT 生成
            wave, y_mel = get_gt_data(
                wave,
                spec,
                ids_slice,
                hps.train.segment_size,
                y_hat.shape[2],
                y_hat_mel.shape[2],
                hps.data.filter_length,
                hps.data.n_mel_channels,
                hps.data.sampling_rate,
                hps.data.hop_length,
                hps.data.win_length,
                hps.data.mel_fmin,
                hps.data.mel_fmax,
                hps.train.fp16_run,
            )

            # トレーニング　Discriminator
            grad_norm_d, loss_disc = train_discriminator(
                discriminator,
                optimizer_discriminator,
                scaler,
                wave,
                y_hat.detach(),
                hps.train.fp16_run,
            )

            # トレーニング　Generator
            grad_norm_g, loss_gen_all, loss_mel, loss_kl, loss_fm, loss_gen = train_generator(
                generator,
                discriminator,
                optimizer_generator,
                scaler,
                wave,
                y_hat,
                (y_mel, y_hat_mel),
                (z_p, logs_q, m_p, logs_p, z_mask),
                hps.train.c_mel * MEL_LOSS_RATIO,
                hps.train.c_kl * KL_LOSS_RATIO,
                hps.train.fp16_run,
            )

            ###############
            # ログ出力とTensorboardに書き込み
            ###############
            if global_step % log_step_interval == 0:
                logger.info(f"Train Epoch: {epoch} [{100.0 * progress_batch_index / len(train_loader):.0f}%]")

                lr = optimizer_generator.param_groups[0]["lr"]
                # Amor For Tensorboard display
                if loss_mel > 75:
                    loss_mel = 75
                if loss_kl > 9:
                    loss_kl = 9

                scalar_dict = {
                    "loss/g/total": loss_gen_all,
                    "loss/g/gen": loss_gen,
                    "loss/g/fm": loss_fm,
                    "loss/g/mel": loss_mel,
                    "loss/g/kl": loss_kl,
                    "learning_rate": lr,
                    "grad_norm_d": grad_norm_d,
                    "grad_norm_g": grad_norm_g,
                }

                # TODO: discriminatorのトレーニングのスキップ状況に応じて、ログ出力要否を変更する
                # if "loss_disc" in locals():
                scalar_dict.update(
                    {
                        "loss/d/total": loss_disc,
                    }
                )
                logger.info(f"loss_disc={loss_disc:.3f}, loss_gen={loss_gen_all:.3f}")
                # else:
                #     logger.info(f"loss_disc=N/A(skip), loss_gen={loss_gen_all:.3f}")

                image_dict = {
                    "slice/mel/pair": plot_2spectrogram_to_numpy(y_mel[0].data.cpu().numpy(), y_hat_mel[0].data.cpu().numpy()),
                }
                summarize(
                    writer=writer,
                    global_step=global_step,
                    images=image_dict,
                    scalars=scalar_dict,
                )

            # バリデーション
            is_last_minibatch = i == len(train_loader)
            if (global_step % val_step_interval == 0 or is_last_minibatch) and val_loader is not None:
                with autocast(enabled=hps.train.fp16_run):
                    generator.eval()
                    discriminator.eval()

                    val_data_iterator = enumerate(val_loader)
                    val_mel_losses = []
                    for batch_idx, info in val_data_iterator:
                        # データアンパック
                        if use_f0:
                            phone, phone_lengths, pitch, pitchf, spec, spec_lengths, wave, wave_lengths, sid = set_next_data(info, device_id, use_f0, cache_gpu)

                        else:
                            phone, phone_lengths, spec, spec_lengths, wave, wave_lengths, sid = set_next_data(info, device_id, use_f0, cache_gpu)
                            pitch = pitchf = None

                        # ジェネレータでwaveformを推論
                        ids_slice, y_hat, y_hat_mel, (z_p, logs_q, m_p, logs_p, z_mask) = process_infer(
                            generator,
                            phone,
                            phone_lengths,
                            pitch,
                            pitchf,
                            spec,
                            spec_lengths,
                            hps.data.filter_length,
                            hps.data.n_mel_channels,
                            hps.data.sampling_rate,
                            hps.data.hop_length,
                            hps.data.win_length,
                            hps.data.mel_fmin,
                            hps.data.mel_fmax,
                            hps.train.fp16_run,
                        )
                        # GT 生成
                        wave, y_mel = get_gt_data(
                            wave,
                            spec,
                            ids_slice,
                            hps.train.segment_size,
                            y_hat.shape[2],
                            y_hat_mel.shape[2],
                            hps.data.filter_length,
                            hps.data.n_mel_channels,
                            hps.data.sampling_rate,
                            hps.data.hop_length,
                            hps.data.win_length,
                            hps.data.mel_fmin,
                            hps.data.mel_fmax,
                            hps.train.fp16_run,
                        )

                        # Loss計算
                        _, y_d_hat_g, fmap_r, fmap_g = discriminator(wave, y_hat)
                        loss_mel = F.l1_loss(y_mel, y_hat_mel) * hps.train.c_mel * MEL_LOSS_RATIO
                        loss_kl = kl_loss(z_p, logs_q, m_p, logs_p, z_mask) * hps.train.c_kl * KL_LOSS_RATIO

                        loss_fm = feature_loss(fmap_r, fmap_g)
                        loss_gen, losses_gen = generator_loss(y_d_hat_g)
                        loss_gen_all = loss_gen + loss_fm + loss_mel + loss_kl
                        val_mel_losses.append(loss_mel.item())
                    val_mel_losses_avr = sum(val_mel_losses) / len(val_mel_losses)
                    scalar_dict = {
                        "val/loss/mel": val_mel_losses_avr,
                    }
                    summarize(
                        writer=writer,
                        global_step=global_step,
                        scalars=scalar_dict,
                    )

            # テスト
            if (global_step % test_step_interval or is_last_minibatch) == 0 and test_loader is not None:
                with autocast(enabled=hps.train.fp16_run):
                    generator.eval()

                    test_data_iterator = enumerate(test_loader)
                    for batch_idx, info in test_data_iterator:
                        # データアンパック
                        if use_f0:
                            phone, phone_lengths, pitch, pitchf, spec, spec_lengths, wave, wave_lengths, sid = set_next_data(info, device_id, use_f0, cache_gpu)

                        else:
                            phone, phone_lengths, spec, spec_lengths, wave, wave_lengths, sid = set_next_data(info, device_id, use_f0, cache_gpu)

                        # ジェネレータでwaveformを推論 (forwardではなくてinferを使う)
                        if use_f0:
                            y_hat, x_mask, (z, z_p, m_p, logs_p) = generator.infer(phone, phone_lengths, pitch, pitchf)
                        else:
                            y_hat, x_mask, (z, z_p, m_p, logs_p) = generator.infer(phone, phone_lengths)

                        # eval_wave_float = wave.float()[:1, :, :]
                        eval_y_hat_float = y_hat.float().detach()[:1, :, :]
                        audio_sampling_rate = sample_rate

                        # Discrmintorで判定
                        # eval_y_d_hat_r, eval_y_d_hat_g, _, _ = discriminator(eval_wave_float, eval_y_hat_float)
                        # eval_loss_gen_r, eval_losses_gen_r = generator_loss(eval_y_d_hat_r)
                        # eval_loss_gen_g, eval_losses_gen_g = generator_loss(eval_y_d_hat_g)

                        # loss_r = (eval_loss_gen_r / len(eval_losses_gen_r)).cpu().detach().numpy()
                        # loss_g = (eval_loss_gen_g / len(eval_losses_gen_g)).cpu().detach().numpy()

                        # print(f"--- Eval(R)({batch_idx}):", loss_r)
                        # print(f"--- Eval(G)({batch_idx}):", loss_g)
                        audio_dict = {
                            f"examples/wav_{batch_idx}": eval_y_hat_float,
                        }
                        summarize(
                            writer=writer,
                            global_step=global_step,
                            audios=audio_dict,
                            audio_sampling_rate=audio_sampling_rate,
                        )

            global_step += 1
            # ミニバッチ終了

        # エポック終了
        scheduler_discriminator.step()
        scheduler_generator.step()
        if callback is not None:
            callback(f"epoch: {epoch:03d}/{n_epochs:03d}", progress_batch_index, iteration_per_epoch, "DONE")

        ###############
        # モデルセーブ
        ###############

        if epoch % save_model_epoch_interval == 0:
            save_checkpoints(
                log_dir,
                generator,
                discriminator,
                optimizer_generator,
                optimizer_discriminator,
                scheduler_generator,
                scheduler_discriminator,
                epoch,
                global_step,
                loss_mel,
                logger,
                sample_rate,
                generator.inter_channels,
                generator.upsample_initial_channel,
                use_f0,
            )
            # logger.info(f"saving ckpt. {project_name} {epoch}")

            if best_mel_loss > val_mel_losses_avr:
                best_mel_loss = val_mel_losses_avr

                save_checkpoints(
                    log_dir,
                    generator,
                    discriminator,
                    optimizer_generator,
                    optimizer_discriminator,
                    scheduler_generator,
                    scheduler_discriminator,
                    epoch,
                    global_step,
                    best_mel_loss,
                    logger,
                    sample_rate,
                    generator.inter_channels,
                    generator.upsample_initial_channel,
                    use_f0,
                    best=True,
                )
                # logger.info(f"saving best ckpt. {project_name} {epoch}")

            if epoch >= total_epoch:
                logger.info("Training is done.")
                # os._exit(0)


def main():
    fire.Fire(train)
