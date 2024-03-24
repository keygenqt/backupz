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
from enum import Enum


# Application texts
class AppTexts(Enum):
    ########
    # Errors
    @staticmethod
    def error_dependency(name: str):
        return '<red>Application</red> "{}" <red>not found, install it.</red>'.format(name)

    @staticmethod
    def error_load_key(key: str):
        return '<red>Error reading configuration file. Check the</red> "{}" <red>parameter.</red>'.format(key)

    @staticmethod
    def error_empty_data():
        return ('<red>Check your configuration file.</red>\n'
                '<yellow>No files were found to archive.</yellow>')

    @staticmethod
    def error_found_folder_for_save(path: str):
        return '<red>Folder for save not found:</red> {}'.format(path)

    @staticmethod
    def error_found_path(path: str):
        return ('<red>Check your configuration file.</red>\n'
                '<yellow>No file or directory found along the path:</yellow> {}').format(path)

    @staticmethod
    def error_connect(method: str, hostname: str):
        return '<red>Error connect {} to</red> "{}" <red>host.</red>'.format(method, hostname)

    @staticmethod
    def error_exception(message: str):
        return '<red>Catch exception: {}</red>'.format(message.strip())

    @staticmethod
    def error_clone_project(url: str):
        return '<red>Git project error clone:</red> {}'.format(url)

    @staticmethod
    def error_download(url: str):
        return '<red>Error download:</red> {}'.format(url)

    ##########
    # Confirms
    @staticmethod
    def confirm_init():
        return 'Add default backupz configuration file?'

    #########
    # Success
    @staticmethod
    def success_init(path: str):
        return '<green>Configuration file added successfully:</green> {}'.format(path)

    @staticmethod
    def success_create_archive(path: str):
        return '<green>Backup successfully created:</green> {}'.format(path)

    @staticmethod
    def success_upload():
        return '<green>Upload successful.</green>'

    @staticmethod
    def success_clone_project(path: str):
        return '<green>Git clone successfully:</green> {}'.format(path)

    @staticmethod
    def success_downloads():
        return '<green>Downloads successful.</green>'

    ######
    # Info
    @staticmethod
    def info_counting():
        return '<blue>Size calculation...</blue>'

    @staticmethod
    def info_start():
        return '<blue>Start creating a backup...</blue>'

    @staticmethod
    def info_upload(method: str, hostname: str):
        return '<blue>Start upload via {}:</blue> {}'.format(method, hostname)

    @staticmethod
    def info_clone_start(url: str):
        return '<blue>Start clone:</blue> {}'.format(url)

    @staticmethod
    def info_download_start(url: str):
        return '<blue>Start download:</blue> {}'.format(url)

    @staticmethod
    def info_download(path: str):
        return '<yellow>File already exist:</yellow> {}'.format(path)

    @staticmethod
    def info_clone_project(path: str):
        return '<yellow>Folder for git repository already exist:</yellow> {}'.format(path)

    @staticmethod
    def info_after_clone(path: str):
        return '<yellow>Empty the folder if you think necessary:</yellow> {}'.format(path)

    @staticmethod
    def info_get_info_video():
        return '<blue>Getting information about a video...</blue>'
