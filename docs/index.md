[![PyPI version](https://badge.fury.io/py/backupz.svg)](https://badge.fury.io/py/backupz)

![picture](images/banner_round.png)

The application helps you create a backup from the necessary files or directories.
The archive is created using [pigz](https://zlib.net/pigz/) - a parallel implementation of gzip for modern multi-processor, multi-core machines.
With cron you can schedule your backups and keep your data intact.
Using the configuration file, you can configure your backups in detail.
You can have several configuration files for different cases.

This is the default configuration file:

```yaml
## Application configuration file Backupz
## Version config: 0.0.5

# Path to file
# - /path/to/you.file
# Path to folder
# - /path/to/folder
# SSH git repo
# - git@github.com:git/ssh.git
# HTTP git repo
# - https://github.com/git/https.git
# Download file by url
# - https://github.com/keygenqt/backupz/raw/main/builds/backupz-2.3.0.pyz
# Download YouTube video, pytube seems to be playing cat and mouse with 1080p resolution
# - https://www.youtube.com/watch?v=N2_7kqSmTZU
backup:
  - ~/.backupz

# Execute command before dump
# Example: mysqldump -u root -p00000 my_db > ~/my_db.sql
execute: []

# https://linux.die.net/man/1/tar
# Exclude by regex (tar --exclude)
exclude: []

# https://linux.die.net/man/1/pigz
# Regulate the speed of compression using the specified digit,
# where -1 or --fast indicates the fastest compression method
# (less compression) and -9 or --best indicates the slowest
# compression method. Level 0 is no compression.
# 1 to 9 or fast/best
compression: best

# Name folder for save backup in format 'datetime.strftime'
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
name: 'backupz_%d_%m_%Y'

# Folder for save
folder: ~/backupz

# Array folders SSH for save
# {
#   hostname: 192.168.2.15
#   username: defaultuser
#   port: 22
#   path: /path/to/folder
#   auth: 'password' or '/path/to/id_rsa'
# }
ssh: []

# Array folders FTP for save
# {
#   hostname: 192.168.2.15
#   username: defaultuser
#   password: '00000'
#   port: 22
#   path: /path/to/folder
# }
ftp: []
```

### License

```
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
```
