import torch

from easy_vc_dev.model.LightweightRVC_Synthesizer_nof0 import EasyVC_Synthesizer_nof0_v1
from easy_vc_dev.model.MultiPeriodDiscriminatorV2 import MultiPeriodDiscriminatorV2


def load_checkpoints(
    checkpoint_path: str,
    generator: EasyVC_Synthesizer_nof0_v1,
    discriminator: MultiPeriodDiscriminatorV2,
    optimizer_generator,
    optimizer_discriminator,
    scheduler_generator,
    scheduler_discriminator,
    logger,
    finetune=False,
):
    logger.info(f"Loading checkpoint from:{checkpoint_path}")

    global_step = 0

    ckpt = torch.load(checkpoint_path, map_location="cpu")
    global_step = ckpt["step"]
    epoch = ckpt["epoch"]
    sample_rate = ckpt["sample_rate"]
    best_mel_loss = float("inf")

    generator.load_state_dict(ckpt["generator"]["model"])
    if not finetune:
        optimizer_generator.load_state_dict(ckpt["generator"]["optimizer"])
        scheduler_generator.load_state_dict(ckpt["generator"]["scheduler"])
        best_mel_loss = ckpt["loss"]

    discriminator.load_state_dict(ckpt["discriminator"]["model"])
    if not finetune:
        optimizer_discriminator.load_state_dict(ckpt["discriminator"]["optimizer"])
        scheduler_discriminator.load_state_dict(ckpt["discriminator"]["scheduler"])
        best_mel_loss = ckpt["loss"]

    return sample_rate, global_step, epoch, best_mel_loss
