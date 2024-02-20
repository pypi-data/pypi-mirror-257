from distutils.core import setup
from setuptools import find_packages

# Note there is no need to setup when
# running locally in this folder.

setup(
    name = "apache-tvm-cu113",
    version = "0.1.0",
    license="Apache-2.0",
    description = "",
    author = "",
    url = "https://github.com/apache/tvm",
    keywords = [],
    packages = find_packages(),
    install_requires = [
        "torch",
        "diffusers",
        "transformers"
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
  ],
)
