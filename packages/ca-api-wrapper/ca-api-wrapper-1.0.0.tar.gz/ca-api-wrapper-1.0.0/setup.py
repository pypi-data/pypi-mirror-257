from setuptools import setup, find_packages

setup(
    name='ca-api-wrapper',
    version='1.0.0',
    author='Vick Mu',
    author_email='arbi3400@gmail.com',
    packages=find_packages(),
    license='LICENSE',
    description='A NON-OFFICIAL Python package for accessing the ChannelAdvisor RESTful API',
    long_description=open('README.md').read(),
    install_requires=[
        # Your package dependencies
    ],
)
