import os
import torch
import json
from easy_vc_dev.model.LightweightRVC_Synthesizer_nof0 import EasyVC_Synthesizer_nof0_v1
from easy_vc_dev.model.MultiPeriodDiscriminatorV2 import MultiPeriodDiscriminatorV2


def save_checkpoint_gen(
    checkpoint_dir: str,
    generator: EasyVC_Synthesizer_nof0_v1,
    epoch: int,
    step: int,
    sample_rate: int,
    use_f0: bool,
    best: bool = False,
):
    state_dict = generator.state_dict()
    new_state_dict = {}

    for key in state_dict.keys():
        if "enc_q" in key:
            continue
        new_state_dict[key] = state_dict[key]

    for k, v in state_dict.items():
        if "module." in k:
            new_state_dict[k[7:]] = v
        else:
            new_state_dict[k] = v
    state_gen = {
        "model": new_state_dict,
        "sample_rate": sample_rate,
        "version": generator.version,
        "f0": use_f0,
    }
    if best:
        if use_f0:
            # checkpoint_path = os.path.join(checkpoint_dir, f"model-f0-best-e{epoch}-s{step}-gen.pt")
            checkpoint_path = os.path.join(checkpoint_dir, "model-f0-best-gen.pt")
        else:
            # checkpoint_path = os.path.join(checkpoint_dir, f"model-nof0-best-e{epoch}-s{step}-gen.pt")
            checkpoint_path = os.path.join(checkpoint_dir, "model-nof0-best-gen.pt")
    else:
        if use_f0:
            checkpoint_path = os.path.join(checkpoint_dir, f"model-f0-e{epoch:04d}-s{step:06d}-gen.pt")
        else:
            checkpoint_path = os.path.join(checkpoint_dir, f"model-nof0-e{epoch:04d}-s{step:06d}-gen.pt")

    torch.save(state_gen, checkpoint_path)


def save_checkpoints(
    checkpoint_dir: str,
    generator: EasyVC_Synthesizer_nof0_v1,
    discriminator: MultiPeriodDiscriminatorV2,
    optimizer_generator,
    optimizer_discriminator,
    scheduler_generator,
    scheduler_discriminator,
    epoch: int,
    step: int,
    loss: float,
    logger,
    sample_rate: int,
    n_mels: int,
    upsample_initial_channel: int,
    use_f0: bool,
    best: bool = False,
):
    state = {
        "generator": {
            "model": generator.state_dict(),
            "optimizer": optimizer_generator.state_dict(),
            "scheduler": scheduler_generator.state_dict(),
        },
        "discriminator": {
            "model": discriminator.state_dict(),
            "optimizer": optimizer_discriminator.state_dict(),
            "scheduler": scheduler_discriminator.state_dict(),
        },
        "step": step,
        "epoch": epoch,
        "loss": loss,
        "version": generator.version,
        "sample_rate": sample_rate,
        "n_mels": n_mels,
        "upsample_initial_channel": upsample_initial_channel,
        "use_f0": use_f0,
    }
    os.makedirs(checkpoint_dir, exist_ok=True)

    if best:
        if use_f0:
            # checkpoint_path = os.path.join(checkpoint_dir, f"model-f0-best-e{epoch}-s{step}.pt")
            checkpoint_path = os.path.join(checkpoint_dir, "model-f0-best.pt")
        else:
            # checkpoint_path = os.path.join(checkpoint_dir, f"model-nof0-best-e{epoch}-s{step}.pt")
            checkpoint_path = os.path.join(checkpoint_dir, "model-nof0-best.pt")
    else:
        if use_f0:
            checkpoint_path = os.path.join(checkpoint_dir, f"model-f0-e{epoch:04d}-s{step:06d}.pt")
        else:
            checkpoint_path = os.path.join(checkpoint_dir, f"model-nof0-e{epoch:04d}-s{step:06d}.pt")

    torch.save(state, checkpoint_path)

    if best:
        data = {"epoch": epoch, "step": step, "loss": loss}
        with open(os.path.join(checkpoint_dir, "best.json"), "w") as json_file:
            json.dump(data, json_file, indent=4)

    save_checkpoint_gen(checkpoint_dir, generator, epoch, step, sample_rate, use_f0, best)

    logger.info(f"Saved checkpoint: {os.path.basename(checkpoint_path)}")
