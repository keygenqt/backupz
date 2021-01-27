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

def gen_default_conf():
    return """### BackupZ2 Configuration Settings
---

### Folders for backup
folders:
  - /path/to/you/folder1
  - /path/to/you/folder2
  - /path/to/you/folder3

### Files for backup
files:
  - /path/to/you/file1
  - /path/to/you/file2
  - /path/to/you/file3
"""
