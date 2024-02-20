from setuptools import setup, find_packages

setup(
    name='arycodes',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'arycodes = arycodes.hello:say_hello'
        ]
    }
)
