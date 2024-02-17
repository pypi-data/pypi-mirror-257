from setuptools import setup, find_packages

setup(
    name='guedesmoney',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'guedesmoney=guedesmoney.main:main'
        ]
    }
)
