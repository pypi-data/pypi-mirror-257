from setuptools import setup, find_packages

setup(
    name='vlookup_mc',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas'
     ],
    author='mohan chinnappan',
    author_email='mohan.chinnappan.n5@gmail.com',
    description='A utility for VLookup between 2 csv files on given fields',
    url='https://github.com/mohan-chinnappan-n/vlookup',
    license='MIT',
)
