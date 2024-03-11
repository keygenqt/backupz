"""
Copyright 2021 Vitaliy Zarubin

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

def gen_default_conf():
    return """### BackupZ2 Configuration Settings
---

# Folders for backup
folders:
  - /path/to/you/folder1
  - /path/to/you/folder2
  - /path/to/you/folder3

# Files for backup
files:
  - /path/to/you/file1
  - /path/to/you/file2
  - /path/to/you/file3

# https://linux.die.net/man/1/pigz
# Regulate the speed of compression using the specified digit #, where -1 or --fast indicates the
# fastest compression method (less compression) and -9 or --best indicates the slowest compression
# method (best compression). Level 0 is no compression.
# 1 to 9 or fast/best
compression: best

# https://linux.die.net/man/1/tar
# Exclude by regex (tar --exclude)
exclude:
  - '*.idea*'

# Name folder for save backup
name: 'backupz_%d_%m_%Y'

# The number of cpu used
processes: 32

# Folder for save
folder: /folder/for/save/backup

# FTP params for save
ftp: user:password@192.168.1.1:/ftp/path/to/your/backup
"""
