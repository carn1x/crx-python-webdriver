# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='crx-python-webdriver',
    version='0.2',
    author='carn1x',
    author_email='github.com/carn1x',
    packages=['crx_python_webdriver'],
    install_requires=[
        'selenium',
    ],
    url='https://github.com/carn1x/crx-python-webdriver',
    license='MIT License, see LICENCE.txt',
    description='Selenium WebDriver framework providing a boilerplate and encouraged design pattern to run on top of' \
                'the WebDriver python bindings.',
    long_description=open('README.md').read(),
    zip_safe=False,
)