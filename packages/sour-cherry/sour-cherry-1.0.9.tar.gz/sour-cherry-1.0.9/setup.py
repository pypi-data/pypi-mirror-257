from setuptools import setup, find_packages

setup(
    name='sour-cherry',
    version='1.0.4',
    packages = find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cherry=src.cherry.cherrypie:cherrypie'
        ],
    },
)