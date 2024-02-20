from setuptools import setup, find_packages

setup(
    name='azure-upload',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'azure-upload=cli.main:main',
        ],
    },
    install_requires=[
        'azure-storage-blob',
    ],
)