# Config Backupz

This is the default configuration file.
This file is used to configure the data backup application.

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
