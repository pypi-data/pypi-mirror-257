
from setuptools import setup, find_packages

with open("README.rst", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="py_stars_tools",
    version="0.0.6",
    packages=find_packages(),
    author="Stars Bing",
    author_email="bing@starsxu.com",
    description="Python 通用工具方法，时间处理、md5、hash处理等",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License"
    ]
)