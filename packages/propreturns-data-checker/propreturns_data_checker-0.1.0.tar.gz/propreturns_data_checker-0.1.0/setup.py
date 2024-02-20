from setuptools import setup, find_packages

setup(
    name="propreturns_data_checker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "sqlalchemy",
    ],
)
