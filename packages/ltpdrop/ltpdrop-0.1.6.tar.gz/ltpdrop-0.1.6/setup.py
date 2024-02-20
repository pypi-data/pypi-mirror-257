from setuptools import setup, find_packages
setup(
name='ltpdrop',
version='0.1.6',
author='martinoo31',
author_email='martimanaresi@gmail.com',
description='LTPDrop is an LTP filter designed to drop/log LTP segments originated by a specific engine',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)