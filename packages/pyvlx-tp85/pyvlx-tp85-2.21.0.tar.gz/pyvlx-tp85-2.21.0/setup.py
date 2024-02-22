"""Module for setting up PyVLX pypi object."""
import os
from os import path

from setuptools import find_packages, setup

REQUIRES = ["PyYAML", "zeroconf"]

PKG_ROOT = os.path.dirname(__file__)

VERSION = "2.21.0"   # basé sur 0.0.21 la version suivante ajoute un reboot auto et permet de zeroconf discovery.


def get_long_description() -> str:
    """Read long description from README.md."""
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, "README.md"), encoding="utf-8") as readme:
        long_description = readme.read()
        return long_description


setup(
    name="pyvlx-tp85",
    version=VERSION,
#    download_url="https://github.com/Julius2342/pyvlx/archive/" + VERSION + ".zip",
#    url="https://github.com/Julius2342/pyvlx",
    url="https://github.com/tipi85/pyvlx-tp85",
    description="PyVLX is a wrapper for the Velux KLF 200 API. It enables run scenes, open, close windows. + SWINGING_SHUTTERS as ROLLER_SHUTTER",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Julius Mittenzwei",
    author_email="julius@mittenzwei.com",
    license="LGPL",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(exclude=['test*']),
    package_data={
        "pyvlx": ["py.typed"],
    },
    python_requires='>=3.11',
    install_requires=REQUIRES,
    keywords="velux KLF 200 home automation",
    zip_safe=False,
)
