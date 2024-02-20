from setuptools import setup, find_packages

setup(
    name='upload_to_azure',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'upload_to_azure = upload_to_azure.cli.main:main',
        ],
    },
)