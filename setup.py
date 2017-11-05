#from distutils.core import setup
from setuptools import setup

setup(
    name='rentright', version='1.0', author='lhennessy',
    author_email='loganjhennessy@gmail.com',
    packages=[
        'rentright',
        'rentright.bin',
        'rentright.flaskapp',
        'rentright.model',
        'rentright.scrape',
        'rentright.scrub', 
        'rentright.utils',
    ],
    install_requires=[
        'bs4',
        'fake_useragent',
        'pandas',
        'pymongo',
        'scikit-learn',
    ],
    url='https://github.com/loganjhennessy/rent-right'
)
