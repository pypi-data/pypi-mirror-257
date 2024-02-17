from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.131'
DESCRIPTION = 'Stupid gamedeveloper games example'

# Setting up
setup(
    name="dclxviclan",
    version=VERSION,
    author="dclxviclan (dclxviclan)",
    author_email="<dclxviclan@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'game', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
