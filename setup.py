from setuptools import setup, find_packages


setup(
    name="python3_lamb",
    version="0.0.1",
    description="advance lib of python usage.",
    author="redrose2100",
    author_email="hitredrose@163.com",
    maintainer="redrose2100",
    maintainer_email="hitredrose@163.com",
    url="https://github.com/redrose2100/python3_lamb",
    install_require=[
        "concurrent-log-handler"
    ],
    license="MIT",
    package=find_packages(),
)