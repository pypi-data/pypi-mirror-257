import os

from setuptools import setup, find_packages

VERSION = '1.0.0'


def _parse_requirements(fname):
    """
    Parse the requirements file and yield the dependency lines.
    :param fname:
    :return:
    """
    with open(fname, encoding="utf-8-sig") as f:
        requirements = f.readlines()
    return requirements


setup(
    name='vistudio-datasource',
    version=VERSION,
    description="sdk in python for vistudio datasource",
    install_requires=_parse_requirements('./requirements.txt'),
    packages=find_packages(exclude=("data_collect", )),
    url='https://console.cloud.baidu-int.com/devops/icode/repos/baidu/bce-vistudio/vistudio-annotation/blob/master',
    python_requires='>=3.6',
)