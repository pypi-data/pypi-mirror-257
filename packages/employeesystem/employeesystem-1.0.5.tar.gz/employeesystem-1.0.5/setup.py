from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
name='employeesystem',
version='1.0.5',
author='Grayson Huey',
author_email='graysonhuey02@gmail.com',
description='Manage your workplace employees',
long_description=long_description,
long_description_content_type='text/markdown',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: Free For Educational Use',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)