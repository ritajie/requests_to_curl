# coding: utf-8

import os
from setuptools import setup, Command


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='requests_to_curl',
    version='1.0.0',
    include_package_data=True,
    install_requires=['requests'],
    license='MIT License',
    description='Library to convert python requests object to curl command.',
    author='Deer',
    author_email='1551755561@qq.com',
    platforms='any',
    url='https://github.com/ritajie/requests_to_curl',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass={
        'clean': CleanCommand,
    },
)
