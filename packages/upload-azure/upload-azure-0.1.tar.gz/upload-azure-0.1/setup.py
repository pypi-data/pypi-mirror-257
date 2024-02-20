from setuptools import setup, find_packages

setup(
    name='upload-azure',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'upload-azure = upload_azure.cli.main:main',
        ],
    },
)