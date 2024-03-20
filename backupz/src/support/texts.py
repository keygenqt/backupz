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
    @staticmethod
    def error_dependency_du():
        return '<red>Application</red> "du" <red>not found, install it.</red>'

    @staticmethod
    def error_dependency_tar():
        return '<red>Application</red> "tar" <red>not found, install it.</red>'

    @staticmethod
    def error_dependency_pigz():
        return '<red>Application</red> "pigz" <red>not found, install it.</red>'

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
    def confirm_init():
        return 'Add default backupz configuration file?'

    @staticmethod
    def success_init(path: str):
        return '<green>Configuration file added successfully:</green> {}'.format(path)

    @staticmethod
    def success_create_archive(path: str):
        return '<green>Backup successfully created:</green> {}'.format(path)

    @staticmethod
    def info_counting():
        return '<blue>Size calculation...</blue>'

    @staticmethod
    def info_start():
        return '<blue>Start creating a backup...</blue>'

    @staticmethod
    def success_upload_ssh(hostname: str):
        return '<green>Upload to ssh</green> "{}" <green>successful.</green>'.format(hostname)

    @staticmethod
    def info_upload_ssh(hostname: str):
        return '<blue>Start downloading via ssh:</blue> {}'.format(hostname)

    @staticmethod
    def error_connect_ssh(hostname: str):
        return '<red>Error connect ssh to</red> "{}" <red>host.</red>'.format(hostname)

    @staticmethod
    def error_exception_ssh(message: str):
        return '<red>Catch exception: {}</red>'.format(message)

    @staticmethod
    def success_upload_ftp(hostname: str):
        return '<green>Upload to ftp</green> "{}" <green>successful.</green>'.format(hostname)

    @staticmethod
    def info_upload_ftp(hostname: str):
        return '<blue>Start downloading via ftp:</blue> {}'.format(hostname)

    @staticmethod
    def error_connect_ftp(hostname: str):
        return '<red>Error connect ftp to</red> "{}" <red>host.</red>'.format(hostname)

    @staticmethod
    def error_exception_ftp(message: str):
        return '<red>Catch exception: {}</red>'.format(message)
