import fire
import torch
import onnx
from onnxsim import simplify
import json
from easy_vc_dev.onnx.LightweightRVC_Synthesizer_nof0_onnx import EasyVC_Synthesizer_nof0_v1_onnx
from typing import Callable


def export_onnx(
    torch_path: str,
    output_path: str,
    static_size: int = 0,
    callback: Callable[[str, int, int, str], None] | None = None,
):
    if callback is not None:
        callback("export", 1, 5, "RUNNING")

    cpt = torch.load(torch_path, map_location="cpu")
    sample_rate = cpt["sample_rate"]
    f0 = cpt["f0"]
    version = cpt["version"]

    model = EasyVC_Synthesizer_nof0_v1_onnx()

    metadata = {
        "application": "EasyVC",
        "version": version,
        "samplingRate": sample_rate,
        "f0": f0,
    }
    print(metadata)

    model.load_state_dict(cpt["model"], strict=False)

    size = static_size if static_size > 0 else 16
    dynamic_axes = (
        {}
        if static_size > 0
        else {
            "feats": [1],
            "pitch": [1],
            "pitchf": [1],
            "audio": [0],  # output
        }
    )

    feats = torch.FloatTensor(1, size, 768).cpu()
    p_len = torch.LongTensor([size]).cpu()
    input_names = ["feats", "p_len"]
    inputs = (
        feats,
        p_len,
    )
    # 出力セットアップ
    output_names = [
        "audio",
    ]

    # 変換処理
    if callback is not None:
        callback("export", 2, 5, "RUNNING")
    torch.onnx.export(
        model,
        inputs,
        output_path,
        dynamic_axes=dynamic_axes,
        do_constant_folding=False,
        opset_version=17,
        verbose=False,
        input_names=input_names,
        output_names=output_names,
    )

    if callback is not None:
        callback("export", 3, 5, "RUNNING")

    model_onnx2 = onnx.load(output_path)
    model_simp, check = simplify(model_onnx2)
    meta = model_simp.metadata_props.add()
    meta.key = "metadata"
    meta.value = json.dumps(metadata)
    if callback is not None:
        callback("export", 4, 5, "RUNNING")
    onnx.save(model_simp, output_path)
    if callback is not None:
        callback("export", 5, 5, "RUNNING")


def main():
    fire.Fire(export_onnx)
