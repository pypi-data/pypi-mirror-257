import fire
from easy_vc_dev.train.train import train
from easy_vc_dev.utils.extract_feature import extract_feats
from easy_vc_dev.utils.generate_filelist import generate_filelist

from easy_vc_dev.utils.preprocess import preprocess

# numbaのwarning回避。（なぞ。）
import logging

numba_logger = logging.getLogger("numba")
numba_logger.setLevel(logging.WARNING)


def main():
    fire.Fire(
        {
            "preprocess": preprocess,
            "extract_feats": extract_feats,
            "generate_filelist": generate_filelist,
            "train": train,
        }
    )


if __name__ == "__main__":
    main()
