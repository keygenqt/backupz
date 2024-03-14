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

from backupz.src.support.helper import get_path_folder, get_path_file
from backupz.src.support.output import echo_stderr
from backupz.src.support.texts import AppTexts


# Create archive with backup
def group_make(ctx: {}):
    """Generate backup."""

    files = []
    folders = []

    # Parse backup file and folder from config
    for item in ctx.obj.get_backup_paths():
        # is a file
        path = get_path_file(item)
        if path:
            files.append(path)
            continue
        # is a folder
        path = get_path_folder(item)
        if path:
            folders.append(path)
            continue
        echo_stderr(AppTexts.error_found_path(item))
        exit(1)

# tar \
# 	--absolute-names \
# 	--use-compress-program="pigz --best --recursive -p 32" \
# 	-cf \
# 	test.tar.gz \
# 	--exclude="*.png" \
# 	/home/keygenqt/Documents/test_backupz/audio.mp3 \
# 	/home/keygenqt/Documents/test_backupz/audio2.mp3 \
# 	/home/keygenqt/Documents/test_backupz/audio3.png

    print(ctx.obj.get_exclude())
    print(ctx.obj.get_compression())
    print(ctx.obj.get_name())
    print(ctx.obj.get_folder_for_save())
    pass
