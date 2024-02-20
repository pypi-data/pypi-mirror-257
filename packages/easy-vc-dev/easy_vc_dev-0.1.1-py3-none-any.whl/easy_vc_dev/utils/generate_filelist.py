import os
from random import shuffle
from typing import Callable
import fire
from easy_vc_dev.const import DATA_TYPE, TRAINER_DIR
from easy_vc_dev.utils.parseBoolArg import parseBoolArg


def generate_filelist(project_name: str, version: int, useF0: bool, sid: int = 0, callback: Callable[[DATA_TYPE, int, int, str], None] | None = None):
    useF0 = parseBoolArg(useF0)
    project_dir = os.path.join(TRAINER_DIR, project_name)

    # フォルダ構成の推定
    project_dir = os.path.join(TRAINER_DIR, project_name)
    train_gt_dir = os.path.join(project_dir, "0_gt_wavs")
    train_f0_dir = os.path.join(project_dir, "2a_f0")
    train_f0nsf_dir = os.path.join(project_dir, "2b_f0nsf")
    train_feat_dir = os.path.join(project_dir, "3_feature768")

    val_gt_dir = os.path.join(project_dir, "0_gt_wavs_val")
    val_f0_dir = os.path.join(project_dir, "2a_f0_val")
    val_f0nsf_dir = os.path.join(project_dir, "2b_f0nsf_val")
    val_feat_dir = os.path.join(project_dir, "3_feature768_val")

    test_gt_dir = os.path.join(project_dir, "0_gt_wavs_test")
    test_f0_dir = os.path.join(project_dir, "2a_f0_test")
    test_f0nsf_dir = os.path.join(project_dir, "2b_f0nsf_test")
    test_feat_dir = os.path.join(project_dir, "3_feature768_test")

    dirs = [
        (train_gt_dir, train_feat_dir, train_f0_dir, train_f0nsf_dir),
        (val_gt_dir, val_feat_dir, val_f0_dir, val_f0nsf_dir),
        (test_gt_dir, test_feat_dir, test_f0_dir, test_f0nsf_dir),
    ]

    # ファイルリスト作成
    for i, (gt_dir, feat_dir, f0_dir, f0nsf_dir) in enumerate(dirs):
        if os.path.exists(gt_dir) is False:
            continue

        # (1) 前処理で作成したファイルがそれぞれ存在することを確認。存在するものだけをトレーニング対象として使う
        if useF0:
            names = set([os.path.splitext(name)[0] for name in os.listdir(gt_dir)]) & set([os.path.splitext(name)[0] for name in os.listdir(feat_dir)]) & set([os.path.splitext(name)[0] for name in os.listdir(f0_dir)]) & set([os.path.splitext(name)[0] for name in os.listdir(f0nsf_dir)])
        else:
            names = set([os.path.splitext(name)[0] for name in os.listdir(gt_dir)]) & set([os.path.splitext(name)[0] for name in os.listdir(feat_dir)])

        # (2) リスト作成
        opt = []
        for name in names:
            if useF0:
                gt_dir = gt_dir.replace("\\", "\\\\")
                feat_dir = feat_dir.replace("\\", "\\\\")
                f0_dir = f0_dir.replace("\\", "\\\\")
                f0nsf_dir = f0nsf_dir.replace("\\", "\\\\")
                opt.append(f"{gt_dir}/{name}.wav|{feat_dir}/{name}.npy|{f0_dir}/{name}.wav.npy|{f0nsf_dir}/{name}.wav.npy|{sid}")
            else:
                gt_wavs_dir = gt_dir.replace("\\", "\\\\")
                feature_dir = feat_dir.replace("\\", "\\\\")
                opt.append(f"{gt_wavs_dir}/{name}.wav|{feature_dir}/{name}.npy|{sid}")
        shuffle(opt)

        # (3) 書き出し
        data_type: DATA_TYPE = "TRAIN" if i == 0 else "VAL" if i == 1 else "TEST"
        suffix = "_val" if data_type == "VAL" else "_test" if data_type == "TEST" else ""
        with open(os.path.join(project_dir, f"filelist{suffix}.txt"), "w") as f:
            f.write("\n".join(opt))
        print("write filelist done")
        if callback is not None:
            callback(data_type, 1, 1, "DONE")


def main():
    fire.Fire(generate_filelist)
