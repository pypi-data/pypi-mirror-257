from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='NEPython',
    version='1.0.0',
    author='TheescapedShadow',
    description='A comprehensive Python library providing essential tools and utilities for streamlined development.',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tqdm',
        'packaging',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    setup_requires=['wheel'],
    include_package_data=True,
)
