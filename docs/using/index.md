# Backupz

The application helps you create a backup from the necessary files or directories.
The archive is created using [pigz](https://zlib.net/pigz/) - a parallel implementation of gzip for modern
multi-processor, multi-core machines.
With cron you can schedule your backups and keep your data intact.
Using the configuration file, you can configure your backups in detail.
You can have several configuration files for different cases.

You can create a backup from:

* Files and directories.
* Git repositories.
* Links to files that will be downloaded in advance.
* You can download and save videos from YouTube.
* The `execute` section allows you to execute commands before the backup, which will allow you to save, for example,
  databases.

You can save the resulting archive in the package specified to you and upload it to the server via FTP or SSH.
