from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from faker import Faker
from tenacity import retry, stop_after_attempt
from tqdm import tqdm

requests.packages.urllib3.disable_warnings()


class Client:
    def __init__(
        self,
        url,
        header={},
        timeout=5,
        proxies=None,
    ):
        """
        Parameters
        ----------

        url: str
            The url of the file to be downloaded.
        header: dict
            The header of the request.
        timeout: float
            Time to wait for the server to send data before giving up.
        proxies: dict
            The proxies of the request.

        Notes
        ----------
        This is a https client.

        Examples
        ----------
        >>> from shakecore.clients.https import Client
        >>> client = Client(url="https://pando-rgw01.chpc.utah.edu/silixa_das_processed_apr_2022_A/SILIXA_78A-32_iDASv3-P13_220423164526_fieldID000110.sgy")
        >>> client.download(threads=4, resume=True)
        >>> client.info()
        """

        self.url = url
        self.header = header
        self.proxies = proxies
        self.timeout = timeout

        if "User-Agent" not in header:
            self.header.setdefault("User-Agent", Faker().user_agent())

        self.check_url()

    @retry(stop=stop_after_attempt(3))
    def check_url(self):
        """
        check url support break-point resume and support multi-threads downloading
        """
        self.flag_resume_and_threads = True

        # verify=False, close ssl double verification, solve the problem of accessing https error
        res = requests.head(
            self.url,
            headers=self.header,
            proxies=self.proxies,
            timeout=self.timeout,
            allow_redirects=True,
            verify=False,
        )

        if not (200 <= res.status_code < 400):
            raise Exception("Bad request!")

        headers = res.headers
        self.file_type = headers.get("Content-Type")
        self.accept_ranges = headers.get("Accept-Ranges")
        self.transfer_encoding = headers.get("Transfer-Encoding")
        self.content_length = int(headers.get("Content-Length", 0))

        # do not support breakpoint resuming and multi-threads downloading
        if (
            self.accept_ranges != "bytes"
            or self.content_length == 0
            or self.transfer_encoding == "chunked"
            or self.transfer_encoding == "gzip, chunked"
        ):
            self.flag_resume_and_threads = False

    def get_range(self, start=0):
        """
        set downloading range
        eg: [(0, 1023), (1024, 2047), (2048, 3071) ...]
        """
        if start == self.content_length:
            _range = [(start, "")]
        else:
            lst = range(start, self.content_length, self.chunk_size)
            _range = list(zip(lst[:-1], [i - 1 for i in lst[1:]]))
            _range.append((lst[-1], ""))

        return _range

    def download_chunk(self, _range):
        start, stop = _range
        headers = {**self.header, **{"Range": f"bytes={start}-{stop}"}}

        res = requests.get(
            self.url,
            headers=headers,
            proxies=self.proxies,
            timeout=self.timeout,
            allow_redirects=True,
            verify=False,
        )
        if res.status_code != 206:
            raise Exception(f"Request raise error, url: {self.url}, range: {_range}")
        return _range, res.content

    @retry(stop=stop_after_attempt(3))
    def download(
        self,
        resume=True,
        threads=1,
        outname=None,
        flag=True,
        chunk_size=1024 * 1000,
    ):
        """
        Parameters
        ----------

        flag: bool
            Whether to show download information.
        resume: bool
            Whether to resume download.
        outname: str
            The name of the file to be saved.
        threads: int
            Number of threads to use for downloading.
        chunk_size: int
            The size of each chunk to download.

        Notes
        ----------
        This is a https client.

        """
        self.resume = resume
        self.threads = threads
        self.outname = Path(outname or self.url.split("/")[-1])
        self.flag = flag
        self.chunk_size = chunk_size

        if self.flag_resume_and_threads is False:
            self.resume = False
            self.threads = 1

            if self.flag:
                print(
                    "Downloading: [not support `breakpoint resuming` and `multi-threads downloading`]"
                )
            res = requests.get(
                self.url,
                headers=self.header,
                proxies=self.proxies,
                timeout=self.timeout,
                allow_redirects=True,
                verify=False,
            )

            if res.status_code != 206:
                raise Exception(f"Request raise error, url: {self.url}")

            open(self.outname, "w").close()
            with open(self.outname, "rb+") as fp:
                fp.seek(0)
                fp.write(res.content)

            if self.flag:
                print("Finished!")
        else:
            if not self.resume:  # if not resume, cover the file from scratch
                start = 0
                open(self.outname, "w+").close()
            else:
                if self.outname.exists():
                    start = self.outname.lstat().st_size
                    # if the file has been downloaded
                    if start == self.content_length:
                        if self.flag:
                            pbar = tqdm(
                                total=self.content_length,
                                initial=start,
                                unit="B",
                                unit_scale=True,
                                desc=f"Downloading via {self.threads} threads",
                                unit_divisor=1024,
                            )
                            pbar.close()
                        return
                else:
                    start = 0
                    open(self.outname, "w+").close()

            # init progress bar
            if self.flag:
                pbar = tqdm(
                    total=self.content_length,
                    initial=start,
                    unit="B",
                    unit_scale=True,
                    desc=f"Downloading via {self.threads} threads",
                    unit_divisor=1024,
                )

            # multi-threads download
            with ThreadPoolExecutor(max_workers=self.threads) as pool:
                res = [
                    pool.submit(self.download_chunk, r)
                    for r in self.get_range(start=start)
                ]

                with open(self.outname, "rb+") as fp:
                    for item in as_completed(res):
                        _range, content = item.result()
                        start, _ = _range
                        fp.seek(start)
                        fp.write(content)
                        if self.flag:
                            pbar.update(self.chunk_size)

            if self.flag:
                pbar.close()

    def info(self):
        print(
            f"""
self.url = {self.url}
self.header = {self.header}
self.timeout = {self.timeout}
self.proxies = {self.proxies}
self.file_type = {self.file_type}
self.accept_ranges = {self.accept_ranges}
self.content_length = {self.content_length}
self.transfer_encoding = {self.transfer_encoding}
self.flag_resume_and_threads = {self.flag_resume_and_threads}
self.resume = {self.resume}
self.threads = {self.threads}
self.outname = {self.outname}
self.flag = {self.flag}
self.chunk_size = {self.chunk_size}
"""
        )
