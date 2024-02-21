from setuptools import setup, find_packages

setup(
    name='ncpcs_common',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'pymysql'
    ]
)