from typing import TypeAlias, Literal


TRAINER_DIR = "trainer"
LRELU_SLOPE = 0.1

DATA_TYPE: TypeAlias = Literal[
    "TRAIN",
    "VAL",
    "TEST",
]
