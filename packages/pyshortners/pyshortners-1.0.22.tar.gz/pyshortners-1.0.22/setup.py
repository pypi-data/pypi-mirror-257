from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.22'
DESCRIPTION = 'An Unofficial API'

# Setting up
setup(
    name="pyshortners",
    version=VERSION,
    author="DK BOTZ",
    license="MIT",
    author_email="dkbotzhelp@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['aiohttp', 'shortzyy'],
    url="https://t.me/DKBOTZ",
    keywords=['python', 'url-shortener'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
