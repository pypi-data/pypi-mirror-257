# Author: Yuto Takizawa <mokoda5243@gmail.com>
# Copyright (c) 2024- Yuto Takizawa
# Licence: MIT

from setuptools import setup

setup(
    name="FastIIIFimageAPI",
    description="iiif ImageAPI for FastAPI",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/WilhelmWeber/IIIFimageAPIforFastAPI",
    license='MIT',
    download_url="https://github.com/WilhelmWeber/IIIFimageAPIforFastAPI",
    author='Yuto_Takizawa',
    author_email="mokoda5243@gmail.com",
    version='0.0.1',
    packages=['iafa'],
    keywords='iiif fastapi',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'pillow>=10.2.0',
        'fastapi>=0.104.1',
    ],
)