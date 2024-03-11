import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='backupz2',
    version='1.0.3',
    author='Vitaliy Zarubin',
    author_email='keygenqt@gmail.com',
    description='Create backup tar.gz archive in multiple processes and send to ftp or save to folder.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/keygenqt/Backupz2",
    packages=setuptools.find_packages(exclude=['*tests.*', '*tests']),
    include_package_data=True,
    py_modules=['colors'],
    install_requires=[
        'click',
        'pyYaml',
    ],
    python_requires='>=3.6',
    entry_points="""
        [console_scripts]
        backupz2 = backupz2.__main__:cli
    """
)
