import fire
import librosa
import json
from easy_vc_dev.utils.whisper.model import Whisper
import numpy as np
from easy_vc_dev.utils.extract_feature import extract_feature_with_whisper
from easy_vc_dev.utils.whisper.whisper import load_model
import onnxruntime
from simple_performance_timer.Timer import Timer
import soundfile as sf
import os


def genereate_input(whisper: Whisper, wav_path: str):
    y, sr = librosa.load(wav_path, sr=16000, dtype="float32")
    feats = extract_feature_with_whisper(whisper, y)
    feats = feats.cpu().numpy()
    feats = np.repeat(feats, 2, axis=1)
    feats_len = feats.shape[1]
    ort_inputs = {
        "feats": feats,
        "p_len": [feats_len],
    }
    return ort_inputs


def infer(onnx_path: str, wav_path: str, thread_num: int = 1):
    whisper_model = "models/embedder/whisper_tiny.pt"
    whisper = load_model(whisper_model).cpu()

    session_options = onnxruntime.SessionOptions()
    session_options.intra_op_num_threads = thread_num
    ort_session = onnxruntime.InferenceSession(
        onnx_path,
        providers=["CPUExecutionProvider"],
        sess_options=session_options,
    )
    modelmeta = ort_session.get_modelmeta()
    metadata = json.loads(modelmeta.custom_metadata_map["metadata"])
    print(metadata)
    for i in ort_session.get_inputs():
        print(i)
    print(ort_session.get_inputs())

    # warmup
    with Timer("warm up x3", True) as _:
        for _ in range(3):
            input = genereate_input(whisper, wav_path)
            _ = ort_session.run(None, input)

    # 推論
    times = 1
    with Timer("infer", True) as t:
        for _ in range(times):
            input = genereate_input(whisper, wav_path)
            t.record("emb")
            output = ort_session.run(None, input)
            t.record("inf")
    print(output[0].shape)
    output_file = os.path.splitext(os.path.basename(wav_path))[0] + "_onnx.wav"
    output_path = os.path.join("output", output_file)
    sf.write(output_path, output[0][0][0], 16000, format="WAV", subtype="FLOAT")


def main():
    fire.Fire(infer)
