"""setup.py file."""

import uuid

from setuptools import setup, find_packages
from pip.req import parse_requirements

__author__ = 'Fernando Garcia <fernando@cutre.net>'

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="napalm-sros",
    version="0.1.0",
    packages=find_packages(),
    author="Fernando Garcia",
    author_email="fernando@cutre.net",
    description="NAPALM driver for SR OS Nokia routers",
    classifiers=[
        'Topic :: Utilities',
         'Programming Language :: Python',
         'Programming Language :: Python :: 2',
         'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    url="https://github.com/napalm-automation/napalm-sros",
    include_package_data=True,
    install_requires=reqs,
)
