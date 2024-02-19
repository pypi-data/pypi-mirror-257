from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))


VERSION = '0.0.6'
DESCRIPTION = 'demo math package for testing'
LONG_DESCRIPTION = 'demo long decription'

# Setting up
setup(
    name="demooMath",
    version=VERSION,
    author="Sanyam Gupta",
    author_email="sanyam233@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="demo long description",
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)