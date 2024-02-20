import urllib.error as ue
import urllib.request as ur
from logging import log, DEBUG
from threading import Thread, Lock
from typing import Union

from tqdm import tqdm

global_mutex = Lock()


class UrlDownloaderThread(Thread):
    """
    A thread class for downloading URLs in parallel. Each thread is responsible for
    downloading a subset of the total URLs based on its index and the total thread counts.
    """

    def __init__(
            self,
            urls: list,
            download_results: list,
            thread_index: int,
            total_threads: int,
            max_attempts: int,
            progress_bar: tqdm,
    ):
        """
        Initializes the UrlDownloaderThread.

        :param urls: The list of URLs to download.
        :param download_results: A shared list to store download results.
        :param thread_index: The index of this thread among all threads.
        :param total_threads: The total number of threads used for downloading.
        :param max_attempts: The maximum number of attempts to download the URL.
        :param progress_bar: A tqdm progress bar to update during downloading.
        """
        super().__init__()
        self.download_results = download_results
        self._urls = urls
        self._thread_index = thread_index
        self._total_threads = total_threads
        self._max_download_attempts = max_attempts
        self._progress_bar = progress_bar
        self._user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68"
        )

    def _download_url(self, url: str) -> Union[bytes, None]:
        """
        Attempts to download the content of the given URL, with up to 'max_attempts' retries for failures.

        :param url: The URL to download.
        :return: The downloaded data.
        :raises: Exception if unable to download the URL after 'max_attempts' attempts.
        """
        request = ur.Request(url, headers={"User-Agent": self._user_agent})
        attempts = 0
        while attempts < self._max_download_attempts:
            try:
                with ur.urlopen(request) as response:
                    return response.read()
            except ue.URLError:
                attempts += 1

        return None

    def run(self):
        """
        The main execution method of the thread. Downloads the assigned URLs and updates shared data.
        """
        for url_index, url in enumerate(self._urls):
            if url_index % self._total_threads == self._thread_index:
                response = self._download_url(url)
                self.download_results[url_index] = response
                if response is not None:
                    if global_mutex.acquire(blocking=True):
                        self._progress_bar.update(1)
                        global_mutex.release()
                else:
                    if global_mutex.acquire(blocking=True):
                        log(
                            level=DEBUG,
                            msg=Exception(
                                f"Failed to download URL after {self._max_download_attempts} attempts: " + url)
                        )
                        global_mutex.release()
                    return
