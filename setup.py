import os
from setuptools import setup, find_packages

try:
    with open("VERSION",encoding="utf-8",mode="r") as f:
        version=f.read().strip()
except:
    version="version is empty"

try:
    with open("README.md",encoding="utf-8",mode="r") as f:
        long_desc=f.read()
except:
    long_desc=""

def find_markdown_files(directory):
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.relpath(os.path.join(root, file), directory))
    return markdown_files

docs_markdown_files = find_markdown_files("docs")

setup(
    name="lambkid",
    version=version,
    description="lambkid is an advance abstract from some common pyton lib, it aim to make you write python more easily and more fewer code.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="redrose2100",
    author_email="hitredrose@163.com",
    maintainer="redrose2100",
    maintainer_email="hitredrose@163.com",
    url="https://github.com/redrose2100/lambkid",
    license="MIT",
    install_requires =[
        "concurrent_log_handler",
        "paramiko"
    ],
    package_data={"": docs_markdown_files},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    packages=find_packages()
)