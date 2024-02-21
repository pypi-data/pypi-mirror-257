from typing import List

from tqdm import tqdm

from odineye.url_downloader.url_downloader_thread import UrlDownloaderThread


class UrlDownloader:
    MAX_DOWNLOAD_THREADS = 128

    def __init__(self, download_threads: int = 8, max_attempts: int = 3):
        """
        Initializes the ParallelUrlDownloader.

        :param download_threads: The number of threads to use for parallel downloading.
        If = -1, then the number of threads is set to the maximum number of threads.
        """
        if download_threads == -1:
            download_threads = UrlDownloader.MAX_DOWNLOAD_THREADS
        assert (
                isinstance(download_threads, int)
                and 1 <= download_threads <= UrlDownloader.MAX_DOWNLOAD_THREADS
        ), f"Downloader can handle from 1 up to {UrlDownloader.MAX_DOWNLOAD_THREADS} threads."
        assert isinstance(max_attempts, int) and max_attempts > 0, "Max attempts must be a positive integer."
        self._download_threads = download_threads
        self._max_download_attempts = max_attempts

    def __call__(self, urls: List[str]) -> List[bytes]:
        """
        Download data from the given URLs.

        :param urls: The list of URLs to download.
        :return: The downloaded data.
        """
        successful_download = True
        data_buffer = [None] * len(urls)
        progress_bar = tqdm(total=len(urls), desc="Downloading URLs")
        threads = [
            UrlDownloaderThread(
                urls,
                data_buffer,
                thread_index,
                self._download_threads,
                self._max_download_attempts,
                progress_bar,
            )
            for thread_index in range(self._download_threads)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        for data in data_buffer:
            if data is None:
                successful_download = False

        return data_buffer, successful_download
