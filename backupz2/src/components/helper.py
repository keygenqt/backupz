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

from pathlib import Path

from backupz2.src.common.default_conf import gen_default_conf


def get_path_home():
    return Path.home()


def get_app_name():
    return 'BackupZ2'


def get_app_version():
    return '1.0.4'


def get_path_conf(conf=None):
    if conf is not None:
        return conf
    else:
        return '{}/.{}.yaml'.format(get_path_home(), get_app_name().lower())


def get_default_conf():
    return gen_default_conf()
