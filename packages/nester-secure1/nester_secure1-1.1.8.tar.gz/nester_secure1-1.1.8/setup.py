from distutils.core import setup
from setuptools import find_packages

setup(
    name='nester_secure1',
    version='1.1.8',
    py_modules=['nester_secure1'],
    packages=find_packages(),
    author='gachomba_eric',
    author_email='gachomba.dev@gmail.com',
    
    url='https://github.com/Gach-omba',
    description='A simple function',
    entry_points={
        "console-scripts":[
            "say_hello = nester_secure1:say_hello"
        ]
    }
)