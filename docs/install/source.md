# Install Backupz from GitHub

This method is suitable for development.

### Create folder

```shell
mkdir -p ~/.local/opt/backupz
```

### Clone project

```shell
git clone https://github.com/keygenqt/backupz.git ~/.local/opt/backupz
```

### Open folder project

```shell
cd ~/.local/opt/backupz
```

### Init environment

```shell
virtualenv .venv
```

### Open environment

```shell
source .venv/bin/activate
```

### Install requirements

```shell
pip install -r requirements.txt
```

### Run app

```shell
python -m backupz
```
