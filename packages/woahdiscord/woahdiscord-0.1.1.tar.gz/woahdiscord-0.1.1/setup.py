from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt', 'r') as file:
    requirements = file.readlines()

setup(
    name='woahdiscord',
    version='0.1.1',
    description='A Python package to create repo and push code on Github',
    author='TAWSIF AHMED',
    author_email='sleeping4cat@outlook.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements
)
