"""
Copyright 2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import time
from multiprocessing.pool import ThreadPool as Pool
from pathlib import Path

import requests
from alive_progress import alive_bar
from requests import Response


# Request with check
def get_request(url: str) -> Response | None:
    try:
        return requests.get(url, stream=True, timeout=3)
    except (Exception,):
        return None


# Download files with progress
# [{'url': url, 'path': download_path}]
def multi_download(download_info: [dict], error_download) -> [Path]:
    # Check is empty
    if not download_info:
        return []

    # Files list
    files = [str(item['path']) for item in download_info]
    files_start_download = []

    # Multidownload length
    total_counter = 0
    total_length = 0

    # Create poll for async
    pool1 = Pool(1)
    pool2 = Pool(len(download_info))

    # Counter length with get (not all head return size in content-length
    def add_length(content_length: int, file: str):
        # values
        nonlocal total_length
        nonlocal total_counter
        nonlocal files_start_download
        # count
        files_start_download.append(file)
        total_length += content_length
        total_counter += 1
        # run progress
        if total_counter == len(download_info):
            pool1.apply_async(_multi_progress, [total_length, files])

    def _error_download(url: str):
        for file in files_start_download:
            Path(file).unlink(missing_ok=True)
        error_download(url)

    # Run download
    for item in download_info:
        pool2.apply_async(_download, [
            item['url'],
            item['path'],
            add_length,
            _error_download
        ])

    pool2.close()
    pool2.join()
    pool1.close()
    pool1.join()

    return files


# Run download file
def _download(url: str, file: Path, content_length, content_error):
    r = get_request(url)
    if not r:
        content_error(url)
        return
    content_length(int(r.headers.get('content-length')), file)
    with get_request(url) as r:
        r.raise_for_status()
        with open(file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)


# Show progress
def _multi_progress(total_length: int, files: []):
    download_length = 0
    with alive_bar(total_length) as bar:
        while download_length < total_length:
            time.sleep(1)
            file_size = 0
            for file in files:
                if os.path.isfile(file):
                    file_stats = os.stat(file)
                    file_size += file_stats.st_size
            add_length = file_size - download_length
            if total_length < add_length + bar.current:
                bar(total_length - bar.current)
                break
            bar(add_length)
            download_length = file_size
