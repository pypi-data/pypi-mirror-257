from typing import Callable, Dict
from easy_vc_dev.utils.Downloader import DOWNLOADER_STATUS, Downloader
import fire


def download_weights(_callback: Callable[[Dict[str, Dict[str, int | str]]], None] | None = None):
    # def callback(param):
    #     print("Callback...", param)

    progresses: Dict[str, Dict[int, int, DOWNLOADER_STATUS]] = {}

    def callback(display_name: str, url: str, n: int, total: int, status: DOWNLOADER_STATUS):
        if url not in progresses:
            progresses[url] = {"display_name": display_name, "n": 0, "total": 0, "status": "RUNNING"}

        if n != -1:
            progresses[url]["n"] = n
        if total != -1:
            progresses[url]["total"] = total

        progresses[url]["display_name"] = display_name
        progresses[url]["status"] = status
        if _callback is not None:
            _callback(progresses)

        # print(progresses)

    downloader = Downloader(callback)

    # Wisper
    downloader.pushItem(
        "whisper_tiny.en.pt",
        "https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt",
        "./models/embedder/whisper_tiny.en.pt",
        "d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03",
    )  # NOQA
    downloader.pushItem(
        "whisper_tiny.pt",
        "https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt",
        "./models/embedder/whisper_tiny.pt",
        "65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9",
    )  # NOQA
    downloader.pushItem(
        "whisper_base.en.pt",
        "https://openaipublic.azureedge.net/main/whisper/models/25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead/base.en.pt",
        "./models/embedder/whisper_base.en.pt",
        "25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead",
    )  # NOQA
    downloader.pushItem(
        "whisper_base.pt",
        "https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt",
        "./models/embedder/whisper_base.pt",
        "ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e",
    )  # NOQA
    # downloader.pushItem(
    #     "https://openaipublic.azureedge.net/main/whisper/models/f953ad0fd29cacd07d5a9eda5624af0f6bcf2258be67c92b79389873d91e0872/small.en.pt",
    #     "./models/embedder/whisper_small.en.pt",
    # )  # NOQA
    # downloader.pushItem(
    #     "https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt",
    #     "./models/embedder/whisper_small.pt",
    # )  # NOQA
    # downloader.pushItem(
    #     "https://openaipublic.azureedge.net/main/whisper/models/d7440d1dc186f76616474e0ff0b3b6b879abc9d1a4926b7adfa41db2d497ab4f/medium.en.pt",
    #     "./models/embedder/whisper_medium.en.pt",
    # )  # NOQA
    # downloader.pushItem(
    #     "https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt",
    #     "./models/embedder/whisper_medium.pt",
    # )  # NOQA

    downloader.download()
    results = downloader.check_hash()
    for r in results:
        if r.status == "NG":
            print(f"Failed to download. url:{r.url}, message:{r.message}")
            callback(r.display_name, r.url, -1, -1, "INVALID")  # nとtotalが-1の時はnとtotalを更新しない。
        else:
            callback(r.display_name, r.url, -1, -1, "VALID")  # nとtotalが-1の時はnとtotalを更新しない。

    return results


def main():
    fire.Fire(
        {
            "weights": download_weights,
        }
    )
