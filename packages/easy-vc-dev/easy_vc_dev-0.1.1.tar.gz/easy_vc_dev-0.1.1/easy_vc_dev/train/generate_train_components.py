import torch
from easy_vc_dev.misc.HParams import HParams2

from easy_vc_dev.model.LightweightRVC_Synthesizer_nof0 import EasyVC_Synthesizer_nof0_v1
from easy_vc_dev.model.MultiPeriodDiscriminatorV2 import MultiPeriodDiscriminatorV2


def generate_train_components(use_f0: bool, hps: HParams2):
    if use_f0:
        pass
        # generator = LightweightRVC_Synthesizer_nof0(
        #     hps.data.filter_length // 2 + 1,  # type: ignore
        #     hps.train.segment_size // hps.data.hop_length,  # type: ignore
        #     # hps.train.segment_size // 256,  # type: ignore
        #     **hps.model,  # type: ignore
        #     is_half=hps.train.fp16_run,  # type: ignore
        #     sr=hps.data.sampling_rate,  # type: ignore
        # )
    else:
        generator = EasyVC_Synthesizer_nof0_v1(
            # hps.data.filter_length // 2 + 1,  # type: ignore
            # hps.train.segment_size // hps.data.hop_length,  # type: ignore
            # # hps.train.segment_size // 256,  # type: ignore
            # **hps.model,  # type: ignore
            # is_half=hps.train.fp16_run,  # type: ignore
            # sr=hps.data.sampling_rate,  # type: ignore
        )

    discriminator = MultiPeriodDiscriminatorV2()

    # オプティマイザ
    optimizer_generator = torch.optim.AdamW(
        generator.parameters(),
        hps.train.learning_rate,
        betas=hps.train.betas,
        eps=hps.train.eps,
    )
    optimizer_discriminator = torch.optim.AdamW(
        discriminator.parameters(),
        hps.train.learning_rate,
        betas=hps.train.betas,
        eps=hps.train.eps,
    )

    # スケジューラ
    scheduler_generator = torch.optim.lr_scheduler.ExponentialLR(optimizer_generator, gamma=hps.train.lr_decay)
    scheduler_discriminator = torch.optim.lr_scheduler.ExponentialLR(optimizer_discriminator, gamma=hps.train.lr_decay)

    return generator, discriminator, optimizer_generator, optimizer_discriminator, scheduler_generator, scheduler_discriminator
