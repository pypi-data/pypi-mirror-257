# Easy VC

簡単、軽量を目的とした音声変換(Voice Conversion)です。

このリポジトリは開発用のリポジトリです。

## Description

## Usage

### トレーニング

#### noF0

ファイルを`raw_data/`に展開しておく。

```bash
poetry run download weights
# ↓ valid_numが全体のデータセットの数を超えないように。
poetry run preprocess --project_name amitaro --wav_dir raw_data/amitaro --valid_num 10 --test_dir raw_data/test_data --sample_rate 16000 --jobs 4
poetry run extract_feature --project_name amitaro --version 1 --device_id 0
poetry run generate_filelist --project_name amitaro --version 1 --useF0 no --sid 0
poetry run train --project_name amitaro --config_path configs/16k_v2.json --sample_rate 16000 --use_f0 False --total_epoch 10 --batch_size 10 --device_id 0 --log_step_interval 10 --val_step_interval 10 --test_step_interval 10 --save_model_epoch_interval 2 --cache_gpu False --freeze_vocoder True


poetry run train --project_name amitaro --config_path configs/16k_v2.json --sample_rate 16000 --use_f0 False --total_epoch 10 --batch_size 10 --device_id 0 --log_step_interval 10 --val_step_interval 10 --test_step_interval 10 --save_model_epoch_interval 2 --cache_gpu False --freeze_vocoder True

poetry run train --project_name amitaro --config_path configs/16k_v2.json --sample_rate 16000 --use_f0 False --total_epoch 1000 --batch_size 10 --device_id 0 --log_step_interval 100 --val_step_interval 100 --test_step_interval 100 --save_model_epoch_interval 50 --cache_gpu False --freeze_vocoder True

# レジューム
poetry run train --project_name amitaro --config_path configs/16k_v2.json --sample_rate 16000 --use_f0 False --total_epoch 10 --batch_size 10 --device_id 0 --log_step_interval 10 --val_step_interval 10 --test_step_interval 10 --save_model_epoch_interval 2 --cache_gpu False --freeze_vocoder True --checkpoint_path trainer/amitaro/logs/model-e4-s432.pt
```

### Export

```bash
poetry run export_onnx --torch_path trainer/sangoku/logs/model-e150-s91050-gen.pt --output_path trainer/sangoku/sangoku.onnx
poetry run export_onnx --torch_path trainer/sangoku/logs/model-nof0-e201-s122007-gen.pt --output_path trainer/sangoku/sangoku.onnx
poetry run infer_with_onnx --onnx_path trainer/sangoku/sangoku.onnx --wav_path raw_data/test_data/queens.wav
```

### pyinstaller

コマンドを１ファイルにする

```bash
poetry run easy_vc preprocess --project_name amitaro --wav_dir raw_data/amitaro --valid_num 10 --test_dir raw_data/test_data --sample_rate 16000 --jobs 4
poetry run easy_vc extract_feats --project_name amitaro --version 1 --device_id 0
poetry run easy_vc generate_filelist --project_name amitaro --version 1 --useF0 no --sid 0
poetry run easy_vc train --project_name amitaro --config_path configs/16k_v2.json --sample_rate 16000 --use_f0 False --total_epoch 10 --batch_size 10 --device_id 0 --log_step_interval 10 --val_step_interval 10 --test_step_interval 10 --save_model_epoch_interval 2 --cache_gpu False --freeze_vocoder True

```

```bash
.venv/bin/pyinstaller  easy_vc_dev/cli.py --onefile  --add-data easy_vc_dev/utils/whisper/assets/*:easy_vc_dev/utils/whisper/assets/
```

```bash
cli preprocess --project_name tsukuyomi --wav_dir raw_data/tsukuyomi --valid_num 10 --test_dir raw_data/test_data --sample_rate 16000 --jobs 4
cli extract_feats --project_name tsukuyomi --version 1 --device_id 0
cli generate_filelist --project_name tsukuyomi --version 1 --useF0 no --sid 0

```

### 音声変換

### リアルタイム音声変換

## Reference

このソフトウェアは次のリポジトリの実装を参考にしています。

[Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
[hifi-gan](https://github.com/jik876/hifi-gan)



### trainの種類

|                               | ckpt | finetune | vocoder_ckpt | discriminator_ckpt |                                                   |
| ----------------------------- | ---- | -------- | ------------ | ------------------ | ------------------------------------------------- |
| 事前学習モデル                |      |          | レ           |                    | 事前学習をするとき                                |
| モデル作成                    | レ   |          |              |                    | 事前学習など既存モデルからの学習                  |
| モデル作成 Finetune           | レ   | レ       |              |                    | 既存モデルからのfinetune(learning rateなどの復帰) |
| モデル作成 vocoder ckpt       | レ   | レ(opt)  | レ           | レ(opt)            | Vocoderを上書き                                   |
| モデル作成 discriminator ckpt | レ   | レ(opt)  | レ(opt)      | レ                 | Discriminatorの上書き(NOT IMPLEMENTED)            |

