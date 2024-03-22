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

from git import Repo

from backupz.src.support.download import multi_download
from backupz.src.support.helper import get_download_folder, pc_command
from backupz.src.support.output import echo_stderr, echo_stdout
from backupz.src.support.progress_alive_bar_git import ProgressAliveBarGit
from backupz.src.support.texts import AppTexts


# Download file
def downloads(urls: [str]) -> [Path]:
    download_files = []
    exist_files = []
    for url in urls:
        # Get path to file
        download_path = get_download_folder() / os.path.basename(url)
        # Check if exist project
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
