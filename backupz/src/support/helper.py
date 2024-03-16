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
import os
import subprocess
from pathlib import Path
from typing import Callable

from cffi.backend_ctypes import unicode


# Get full path folder
def get_path_folder(
        path: str
) -> Path | None:
    path = get_path_file(path, False)
    if path.is_dir():
        return path
    else:
        return None


# Get full path file
def get_path_file(
        path: str,
        none: bool = True,
        starting: str = None
) -> Path | None:
    if not path:
        return None

    if not starting:
        starting = os.getcwd()

    # Format path
    if path.startswith('~/'):
        path = os.path.expanduser(path)
    if path.startswith('./'):
        path = '{}{}'.format(starting, path[1:])
    if path.startswith('../'):
        path = '{}/{}'.format(starting, path)

    # Read path
    path = Path(path)

    if none and not path.is_file():
        return None

    return Path(path)


# Common run pc command
def pc_command(
        args: [],
        callback: Callable[[str, int], None] = None,
) -> []:
    is_error = False
    result = []

    def output(value: any, i: int) -> bool:
        result.append(value)
        if callback:
            callback(value, i)
        else:
            return False

    try:
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
            index = 1
            for line in iter(lambda: process.stdout.readline(), ""):
                if not line:
                    break
                line = unicode(line.rstrip(), "utf-8")
                is_error = output(line, index)
                index += 1

    except Exception as e:
        is_error = output(str(e), len(result))

    if is_error:
        exit(1)

    return result
