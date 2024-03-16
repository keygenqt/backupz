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
import subprocess

from backupz.src.support.output import echo_stderr
from backupz.src.support.texts import AppTexts


# Check dependency for init
def check_dependency_init():
    # Check git application
    try:
        subprocess.run(['du', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_du())
        exit(1)

    # Check tar application
    try:
        subprocess.run(['tar', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_tar())
        exit(1)

    # Check pigz application
    try:
        subprocess.run(['pigz', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_pigz())
        exit(1)
