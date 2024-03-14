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


# Create archive with backup
def group_make(ctx: {}):
    """Generate backup."""
    print(ctx.obj.get_backup_paths())
    print(ctx.obj.get_exclude())
    print(ctx.obj.get_compression())
    print(ctx.obj.get_name())
    print(ctx.obj.get_folder_for_save())
    pass
