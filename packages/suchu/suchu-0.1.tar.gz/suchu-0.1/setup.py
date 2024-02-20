from setuptools import setup, find_packages

setup(
    name='suchu',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'suchu = suchu.hello:say_hello'
        ]
    }
)
