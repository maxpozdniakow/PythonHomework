from setuptools import setup, find_packages

setup(
    name='pycalc',
    description='pure line-command calculator',
    version='ver:0.9',
    author='Maxon',
    author_email='asd@asd.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pycalc = calculator.pycalc:main']
    }
)
