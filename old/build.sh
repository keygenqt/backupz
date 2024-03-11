#!/usr/bin/env bash

version=$(grep version setup.py | sed "s/ //g" | sed "s/',//g" | sed "s/version='//g")

# clean old build
rm -r dist build ./*.egg-info ./*.pyz

# build python
python3 setup.py sdist bdist_wheel

# include app
pip3 install . --target dist/

# finally, build!
shiv --site-packages dist --compressed -p '/usr/bin/env python3' -o backupz2-"$version".pyz -e backupz2.__main__:cli
