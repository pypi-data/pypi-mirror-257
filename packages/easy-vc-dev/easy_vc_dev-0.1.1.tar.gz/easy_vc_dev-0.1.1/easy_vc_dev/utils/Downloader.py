from dataclasses import dataclass
import os
from time import sleep
import requests
from concurrent.futures import ThreadPoolExecutor
import hashlib
from typing import Callable, List

from typing import TypeAlias, Literal


def is_running_on_colab():
    try:
        import google.colab  # NOQA

        return True
    except ImportError:
        return False


if is_running_on_colab():
    print("load tqdm for notebook")
    from tqdm.notebook import tqdm
else:
    #    print("load normal notebook")
    from tqdm import tqdm


@dataclass
class DownloadParams:
    display_name: str
    url: str
    saveTo: str
    hash: str | None
    position: int


@dataclass
class HashCheckResult:
    display_name: str
    url: str
    status: str
    message: str


DOWNLOADER_STATUS: TypeAlias = Literal[
    "RUNNING",
    "DOWNLOADED",
    "VALID",
    "INVALID",
]


class Downloader:
    def __init__(self, callback: Callable[[str, str, int, int, DOWNLOADER_STATUS], None] | None = None):
        self.callback = callback
        self.params: list[DownloadParams] = []

    def pushItem(self, display_name: str, url: str, saveTo: str, hash: str | None):
        self.params.append(DownloadParams(display_name, url, saveTo, hash, len(self.params)))

    def download(self):
        with ThreadPoolExecutor() as pool:
            pool.map(self._downloadItem, self.params)
        sleep(1)

    def _downloadItem(self, params: DownloadParams):
        display_name = params.display_name
        url = params.url
        saveTo = params.saveTo
        position = params.position
        dirname = os.path.dirname(saveTo)
        if dirname != "":
            os.makedirs(dirname, exist_ok=True)

        try:
            req = requests.get(url, stream=True, allow_redirects=True)

            content_length_header = req.headers.get("content-length")
            content_length = int(content_length_header) if content_length_header is not None else 1024 * 1024 * 1024

            progress_bar = tqdm(
                total=content_length if content_length > 0 else None,
                leave=False,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                position=position,
            )

            # with tqdm
            chunk_num = content_length // 1024
            callbacl_interval = chunk_num // 100
            with open(saveTo, "wb") as f:
                for i, chunk in enumerate(req.iter_content(chunk_size=1024)):
                    if chunk:
                        progress_bar.update(len(chunk))
                        if self.callback is not None:
                            if i % callbacl_interval == 0:
                                self.callback(display_name, url, progress_bar.n, progress_bar.total, "RUNNING")
                        f.write(chunk)

            if self.callback is not None:
                self.callback(display_name, url, progress_bar.n, progress_bar.total, "DOWNLOADED")

        except Exception as e:
            print(e)

    def check_hash(self):
        results: List[HashCheckResult] = []
        for target in self.params:
            if not os.path.exists(target.saveTo):
                result = HashCheckResult(target.display_name, target.url, "NG", "file not found")
                results.append(result)
                continue

            with open(target.saveTo, "rb") as f:
                data = f.read()
                hash = hashlib.sha256(data).hexdigest()
                if hash != target.hash:
                    result = HashCheckResult(target.display_name, target.url, "NG", f"hash not match, expected: {target.hash}, actual: {hash}")
                    results.append(result)
                else:
                    result = HashCheckResult(target.display_name, target.url, "OK", "hash match")
                    results.append(result)
        return results
