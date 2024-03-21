# Install Backupz *.pyz

This method is as simple as possible - the entire application is in a pyz file.

### Create folder

```shell
mkdir ~/.local/opt
```

### Download

```shell
wget -x https://github.com/keygenqt/backupz/raw/main/builds/backupz-2.1.0.pyz \
  -O ~/.local/opt/backupz.pyz
```

### Add alias to `~/.bashrc`

```shell
alias backupz='python3 ~/.local/opt/backupz.pyz'
```

### Update environment

```shell
source ~/.bashrc
```
