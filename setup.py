"""
Setup script for the logdash package.
"""

from setuptools import setup, find_packages
import re

# Read version from __init__.py
with open('logdash/__init__.py', 'r') as f:
    version_match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError('Cannot find version information')

setup(
    name="logdash",
    version=version,
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "colorama>=0.4.4",
    ],
    author="logdash",
    author_email="info@logdash.io",
    description="Python SDK for logdash logging and metrics service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="logging, metrics, monitoring",
    url="https://logdash.io",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.7",
) 