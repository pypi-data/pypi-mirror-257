from setuptools import setup, find_packages

setup(
    name='base_convertor',
    version='0.5.1',
    author='Ajay Maurya',
    author_freeCodeCamp_username="IAMAJAYPRO",

    description='A package for converting numbers from one base to another.',
    packages=find_packages(),
    # Other setup configurations...
    entry_points={
        'console_scripts': [
            'base-convert = base_convertor:convert_base',
        ],
    }
)
