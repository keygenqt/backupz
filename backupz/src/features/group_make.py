"""
Copyright 2021-2024 Vitaliy Zarubin

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
import multiprocessing
import shutil

from backupz.src.features.impl.utils import git_clone, get_size_blocks, downloads, youtube_download
from backupz.src.support.conf import Conf
from backupz.src.support.dependency import check_dependency_git, check_dependency_ffmpeg
from backupz.src.support.helper import get_path_folder, get_path_file, pc_command, get_download_folder
from backupz.src.support.output import echo_stderr, echo_stdout
from backupz.src.support.progress_alive_bar import ProgressAliveBar
from backupz.src.support.texts import AppTexts


# Create archive with backup
def group_make(config: Conf, is_delete_temp: bool):
    """Generate backup."""

    # Execute command before dump
    for command in config.get_execute_commands():
        import subprocess
        try:
            subprocess.run(command, check=True, shell=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            echo_stderr(AppTexts.error_exception(str(e)))
            exit(1)

    # Exclude files by regex
    excludes = ['--exclude={}'.format(exclude) for exclude in config.get_exclude()]

    gits = []
    urls = []
    youtube = []
    files = []
    folders = []

    # Parse backup file and folder from config
    for item in config.get_backup_paths():
        # Check is link YouTube
        if 'youtu.be' in item or 'youtube.com' in item:
            check_dependency_ffmpeg()
            youtube.append(item)
            continue
        # Check is git repos
        if '.git' in item and ('git@' in item or 'https' in item):
            check_dependency_git()
            gits.append(item)
            continue
        # Check is url
        if 'http://' in item or 'https://' in item:
            urls.append(item)
            continue
        # is a file
        path = get_path_file(item)
        if path:
            files.append(str(path))
            continue
        # is a folder
        path = get_path_folder(item)
        if path:
            folders.append(str(path))
            continue
        echo_stderr(AppTexts.error_found_path(item))
        exit(1)

    # Run clone repos
    for item in gits:
        path = git_clone(item)
        if not path:
            echo_stderr(AppTexts.error_clone_project(item))
            exit(1)
        else:
            folders.append(str(path))

    # Run download video youtube
    for item in youtube:
        path = youtube_download(item)
        if not path:
            echo_stderr(AppTexts.error_download(item))
            exit(1)
        else:
            files.append(str(path))

    # Run multi downloads
    files = files + downloads(urls)

    if not files and not folders:
        echo_stderr(AppTexts.error_empty_data())
        exit(1)

    echo_stdout(AppTexts.info_counting())

    # Get total size for progress
    total_size_blocks = 0
    for item in files:
        total_size_blocks += get_size_blocks(item, excludes)
    for item in folders:
        total_size_blocks += get_size_blocks(item, excludes)

    # Create ssh bar
    bar = ProgressAliveBar()

    def update_bar(out):
        if 'tar:' in out:
            blocks = int(out.replace('tar: #', ''))
            if blocks < total_size_blocks:
                bar.update(blocks, total_size_blocks)
        elif 'Total bytes written:' in out:
            bar.update(total_size_blocks, total_size_blocks)
        else:
            echo_stderr(out)
            exit(1)

    echo_stdout(AppTexts.info_start())

    pc_command([
                   'tar',
                   '--record-size=1K',
                   '--checkpoint={}'.format(int(total_size_blocks / 50)),
                   '--absolute-names',
                   '--use-compress-program',
                   'pigz {compression} --recursive -p {cpu_count}'.format(
                       compression=config.get_compression(),
                       cpu_count=multiprocessing.cpu_count()
                   ),
                   '-cf',
                   str(config.get_path_to_save()),
                   '--totals',
                   '--checkpoint-action=echo="#%u"',
               ] + excludes + files + folders, callback=lambda out, _: update_bar(out))

    echo_stdout(AppTexts.success_create_archive(str(config.get_path_to_save())))

    # Upload to ssh
    for ssh in config.get_data_ssh():
        ssh.upload(config.get_path_to_save())

    # Upload to ftp
    for ftp in config.get_data_ftp():
        ftp.upload(config.get_path_to_save())

    # Info abot cache
    if not is_delete_temp and (gits or urls):
        echo_stdout(AppTexts.info_after_clone(str(get_download_folder())))

    # Delete files if need
    if is_delete_temp:
        shutil.rmtree(get_download_folder(), ignore_errors=True)
