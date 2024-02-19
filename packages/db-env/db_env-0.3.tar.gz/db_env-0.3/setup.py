from setuptools import setup, find_packages

with open('README.txt', 'r') as f:
    long_description = f.read()

setup(
    name=           'db_env',
    version=        '0.3',
    description=    'library that creates a relational database with the usage of SQLite. More information follows.',
    author=         'Daniel Huber',
    packages=find_packages(),
    long_description=long_description, 
    long_description_content_type='text/plain',
)

