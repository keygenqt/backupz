BackupZ2
===================

![picture](data/icon-160.png)

***Version**: 1.0.1*

Create **backup** tar.gz archive in multiple processes and send to ftp or save to folder.

#### Basic functionality

* Backup folders
* Backup files
* Exclude by regex (tar --exclude)
* Multiple processes

#### Save

* Save to folder
* Save to ftp

### Install

#### pyz

```shell
wget https://github.com/keygenqt/BackupZ2/raw/master/data/backupz2.pyz
```

```shell
# backup to folder
python3 backupz2.pyz folder

# backup to FTP
python3 backupz2.pyz ftp
```

#### snap

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/backupz2)

```shell
sudo snap install --devmode backupz2
```

```shell
# backup to folder
backupz2 folder

# backup to FTP
backupz2 ftp
```

### Preview

![picture](data/preview.png)

