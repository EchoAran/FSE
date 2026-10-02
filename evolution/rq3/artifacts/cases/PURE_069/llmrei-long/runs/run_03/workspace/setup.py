from setuptools import setup, find_packages

setup(
    name='pdfsplitmerge',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['pypdf'],
    entry_points={'console_scripts': ['pdfsplitmerge=pdfsplitmerge.__main__:main']},
)
