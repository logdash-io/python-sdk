"""
Setup script for the LogDash package.
"""

from setuptools import setup, find_packages

setup(
    name="logdash",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "colorama>=0.4.4",
    ],
    author="LogDash",
    author_email="info@logdash.io",
    description="Python SDK for LogDash logging and metrics service",
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