from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='run_as_admin',
    version='1.7.0',
    packages=find_packages(),
    author='Barno Chakraborty',
    author_email='barno.baptu@gmail.com',
    description='This script provides a simple way to execute a file as an administrator on Windows systems.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/barno1994/runasadmin',
    # Add the following line to support creating wheel distributions
    setup_requires=['wheel']
)