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

from backupz.src.support.conf import Conf
from backupz.src.support.helper import get_path_folder, get_path_file, pc_command
from backupz.src.support.output import echo_stderr, echo_stdout
from backupz.src.support.progress_alive_bar import ProgressAliveBar
from backupz.src.support.texts import AppTexts


# Get block size file or folder
def _get_size_blocks(path_data: str, excludes: []) -> int | None:
    result = pc_command([
                            'du',
                            '-sk',
                        ] + excludes + [path_data])
    find = [data.replace(path_data, '').strip() for data in result if path_data in data]
    if find:
        return int(find[0])
    else:
        return None


# Create archive with backup
def group_make(config: Conf):
    """Generate backup."""

    # Exclude files by regex
    excludes = ['--exclude={}'.format(exclude) for exclude in config.get_exclude()]

    files = []
    folders = []

    # Parse backup file and folder from config
    for item in config.get_backup_paths():
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

    if not files and not folders:
        echo_stderr(AppTexts.error_empty_data())
        exit(1)

    echo_stdout(AppTexts.info_counting())

    # Get total size for progress
    total_size_blocks = 0
    for item in files:
        total_size_blocks += _get_size_blocks(item, excludes)
    for item in folders:
        total_size_blocks += _get_size_blocks(item, excludes)

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
