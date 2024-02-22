from setuptools import find_packages
from setuptools import setup

setup(
    name="remote-pykernel",
    version="0.0.1",
    license="GNU General Public License v2.0",
    author="Talaviya Bhavik",
    author_email="talaviyabhavik@proton.me",
    description="A remote ipykernel for JupyterLab",
    packages=find_packages("remote_pykernel"),
    package_dir={"": "remote_pykernel"},
    url="https://github.com/imnotdev25/remote-ipykernel",
    project_urls={
        "Bug Report": "https://github.com/imnotdev25/remote-ipykernel/issues/new",
    },
    install_requires=[
        'jupyterlab',
        'ipykernel',
        'tornado',
        'remote_ipykernel_interrupt',
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    py_modules=["remote_pykernel"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)