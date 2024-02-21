from setuptools import setup, find_packages

setup(
    name='azure-uploading',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'azure-uploading = upload_azure.cli.main:main',
        ],
    },
)