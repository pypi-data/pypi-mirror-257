import torch
from torch.utils.data import DataLoader
from typing import List, Any


def generate_gpu_cache(use_f0: bool, device_id: int, train_loader: DataLoader):
    cache: List[Any] = []
    for batch_idx, info in enumerate(train_loader):
        # Unpack
        if use_f0:
            (phone, phone_lengths, pitch, pitchf, spec, spec_lengths, wave, wave_lengths, sid) = info
        else:
            (phone, phone_lengths, spec, spec_lengths, wave, wave_lengths, sid) = info
        # Load on CUDA
        if torch.cuda.is_available():
            phone = phone.cuda(device_id, non_blocking=True)
            phone_lengths = phone_lengths.cuda(device_id, non_blocking=True)
            if use_f0:
                pitch = pitch.cuda(device_id, non_blocking=True)
                pitchf = pitchf.cuda(device_id, non_blocking=True)
            sid = sid.cuda(device_id, non_blocking=True)
            spec = spec.cuda(device_id, non_blocking=True)
            spec_lengths = spec_lengths.cuda(device_id, non_blocking=True)
            wave = wave.cuda(device_id, non_blocking=True)
            wave_lengths = wave_lengths.cuda(device_id, non_blocking=True)
        # Cache on list
        if use_f0:
            cache.append((batch_idx, (phone, phone_lengths, pitch, pitchf, spec, spec_lengths, wave, wave_lengths, sid)))
        else:
            cache.append((batch_idx, (phone, phone_lengths, spec, spec_lengths, wave, wave_lengths, sid)))
    return cache
