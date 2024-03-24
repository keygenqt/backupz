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
from pathlib import Path

import requests
from git import Repo
from pytube import YouTube, extract

from backupz.src.support.download import multi_download
from backupz.src.support.helper import get_download_folder, pc_command
from backupz.src.support.output import echo_stderr, echo_stdout
from backupz.src.support.progress_alive_bar import ProgressAliveBar
from backupz.src.support.progress_alive_bar_git import ProgressAliveBarGit
from backupz.src.support.texts import AppTexts


# Download video from youtube
def youtube_download(url: str) -> Path | None:
    try:
        bar = ProgressAliveBar(AppTexts.success_downloads())

        def on_complete_callback(stream, event):
            # Download image preview max size
            try:
                image_path = get_download_folder() / stream.default_filename.replace('.mp4', '') / 'maxresdefault.jpg'
                image_url = 'https://i.ytimg.com/vi/{}/maxresdefault.jpg'.format(extract.video_id(url))
                r = requests.get(image_url, allow_redirects=True)
                open(image_path, 'wb').write(r.content)
            except (Exception,):
                pass
            # End progress
            bar.spinner_end()

        # Get YouTube video
        echo_stdout(AppTexts.info_get_info_video())
        yt = YouTube(url, on_complete_callback=on_complete_callback)
        # Get path to file
        download_path = get_download_folder() / yt.streams.first().default_filename.replace('.mp4', '')
        # Check if exist file
        if download_path.is_dir():
            echo_stderr(AppTexts.info_download(str(download_path.absolute())))
            return download_path
        else:
            echo_stdout(AppTexts.info_download_start(url))
            bar.spinner_start()
            # Download max resolution
            (yt.streams
             .filter(progressive=True, file_extension='mp4')
             .order_by('resolution')
             .desc()
             .first()
             .download(output_path=download_path))
            return download_path
    except (Exception,):
        pass
    return None


# Download file
def downloads(urls: [str]) -> [Path]:
    download_files = []
    exist_files = []
    for url in urls:
        # Get path to file
        download_path = get_download_folder() / os.path.basename(url)
        # Check if exist file
        if download_path.is_file():
            echo_stderr(AppTexts.info_download(str(download_path.absolute())))
            exist_files.append(str(download_path))
        else:
            echo_stdout(AppTexts.info_download_start(url))
            download_files.append({'url': url, 'path': download_path})

    def catch_error(error_url):
        echo_stderr(AppTexts.error_download(error_url))
        os._exit(1)  # noqa

    download_files = multi_download(download_files, catch_error)
    if download_files:
        echo_stdout(AppTexts.success_downloads())
    return download_files + exist_files


# Clone git project
def git_clone(url: str) -> Path | None:
    # Get path
    clone_path = get_download_folder() / os.path.basename(url).replace('.git', '')

    # Check if path file
    if clone_path.is_file():
        return None

    # Check if exist project
    if clone_path.is_dir():
        echo_stderr(AppTexts.info_clone_project(str(clone_path.absolute())))
    else:
        echo_stdout(AppTexts.info_clone_start(url))
        try:
            Repo.clone_from(
                url=url,
                to_path=clone_path,
                progress=ProgressAliveBarGit(AppTexts.success_clone_project(clone_path))  # noqa
            )
        except (Exception,):
            return None

    return clone_path


# Get block size file or folder
def get_size_blocks(path_data: str, excludes: []) -> int | None:
    result = pc_command([
                            'du',
                            '-sk',
                        ] + excludes + [path_data])
    find = [data.replace(path_data, '').strip() for data in result if path_data in data]
    if find:
        return int(find[0])
    else:
        return None
