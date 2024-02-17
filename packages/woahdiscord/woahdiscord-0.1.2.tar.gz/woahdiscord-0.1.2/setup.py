from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt', 'r') as file:
    requirements = file.readlines()

setup(
    name='woahdiscord',
    version='0.1.2',
    description='A python library allowing discord to be used unlimited cloud storage. ',
    author='TAWSIF AHMED',
    author_email='sleeping4cat@outlook.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements
)
