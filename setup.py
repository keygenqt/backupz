import setuptools

long_description = """
![picture](https://github.com/keygenqt/backupz/blob/main/data/banners/banner_round.png?raw=true)

Create and save a backup archive in multiple processes.

[More...](https://keygenqt.github.io/backupz)

### License

```
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
```
"""

setuptools.setup(
    name='backupz',
    version='2.0.0.1',
    author='Vitaliy Zarubin',
    author_email='keygenqt@gmail.com',
    description='The application allows you to generate CHANGELOG files based on Git tags.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/keygenqt/backupz",
    packages=setuptools.find_packages(exclude=['*tests.*', '*tests']),
    include_package_data=True,
    py_modules=['colors'],
    install_requires=[
        'click>=8.1.7',
        'pyYaml>=6.0.1',
        'cffi>=1.16.0',
        'beautifulsoup4>=4.12.3',
        'alive-progress>=3.1.5',
    ],
    python_requires='>=3.8.2',
    entry_points="""
        [console_scripts]
        backupz = backupz.__main__:main
    """
)
