import torch
from torch.utils.data import DataLoader

import os
from easy_vc_dev.misc.HParams import HParams2
from easy_vc_dev.train.components.data_utils import DistributedBucketSampler, TextAudioCollate, TextAudioCollateMultiNSFsid, TextAudioLoaderMultiNSFsid, TextAudioLoader


def generate_data_loader(project_dir: str, use_f0: bool, batch_size: int, hps: HParams2):
    # トレーニングデータセットのローダー
    train_files = os.path.join(project_dir, "filelist.txt")
    if use_f0:
        train_dataset: torch.utils.data.Dataset = TextAudioLoaderMultiNSFsid(train_files, hps.data)  # type: ignore
    else:
        train_dataset = TextAudioLoader(train_files, hps.data)  # type: ignore

    train_sampler = DistributedBucketSampler(  # 単一GPUで動作を想定して、gpuの数は１で計算している。
        train_dataset,
        batch_size,  # type: ignore
        [100, 200, 300, 400, 500, 600, 700, 800, 900],
        num_replicas=1,
        rank=0,
        shuffle=True,
    )

    if use_f0:
        collate_fn: TextAudioCollate | TextAudioCollateMultiNSFsid = TextAudioCollateMultiNSFsid()
    else:
        collate_fn = TextAudioCollate()

    train_loader = DataLoader(
        train_dataset,
        num_workers=4,
        shuffle=False,
        pin_memory=True,
        collate_fn=collate_fn,
        batch_sampler=train_sampler,
        persistent_workers=True,
        prefetch_factor=8,
    )

    # Valデータセットのローダー
    val_files = os.path.join(project_dir, "filelist_val.txt")
    if os.path.exists(val_files):
        if use_f0:
            val_dataset: torch.utils.data.Dataset = TextAudioLoaderMultiNSFsid(val_files, hps.data)  # type: ignore
        else:
            val_dataset = TextAudioLoader(val_files, hps.data)  # type: ignore

        val_sampler = DistributedBucketSampler(  # 単一GPUで動作を想定して、gpuの数は１で計算している。
            val_dataset,
            batch_size,  # type: ignore
            [100, 200, 300, 400, 500, 600, 700, 800, 900],
            num_replicas=1,
            rank=0,
            shuffle=False,
        )

        # if use_f0:
        #     collate_fn_forval: TextAudioCollate | TextAudioCollateMultiNSFsid = TextAudioCollateMultiNSFsid()
        # else:
        #     collate_fn_forval = TextAudioCollate()

        val_loader = DataLoader(
            val_dataset,
            num_workers=4,
            shuffle=False,
            pin_memory=True,
            collate_fn=collate_fn,
            batch_sampler=val_sampler,
            persistent_workers=True,
            prefetch_factor=8,
        )
    else:
        val_loader = None

    # テストデータセットのローダー
    test_files = os.path.join(project_dir, "filelist_test.txt")
    if os.path.exists(test_files):
        if use_f0:
            test_dataset: torch.utils.data.Dataset = TextAudioLoaderMultiNSFsid(test_files, hps.data)  # type: ignore

        else:
            test_dataset = TextAudioLoader(test_files, hps.data)  # type: ignore

        test_sampler = DistributedBucketSampler(  # 単一GPUで動作を想定して、gpuの数は１で計算している。
            test_dataset,
            1,  # type: ignore
            [100, 200, 300, 400, 500, 600, 700, 800, 90000],
            num_replicas=1,
            rank=0,
            shuffle=True,
        )
        test_loader = DataLoader(
            test_dataset,
            num_workers=4,
            shuffle=False,
            pin_memory=True,
            collate_fn=collate_fn,
            batch_sampler=test_sampler,
            persistent_workers=True,
            prefetch_factor=8,
        )
    else:
        test_loader = None

    return train_loader, val_loader, test_loader, train_sampler
