from setuptools import setup, find_packages


NAME = 'fastgcf'
VERSION = '1.0.6'
DESCRIPTION = 'FastAPI in Google Cloud Functions'
AUTHOR = 'Tigran Zalian'
AUTHOR_EMAIL = 'tigraanzalian@gmail.com'
URL = 'https://github.com/TigranZalian/fastgcf'

with open('./requirements.txt', 'r') as f:
    INSTALL_REQUIRES = list(filter(lambda l: bool(l.strip()), f.readlines()))

PACKAGES = find_packages()

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
]

with open('README.md', 'r', encoding='utf-8') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    classifiers=CLASSIFIERS,
)
