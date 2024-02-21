from setuptools import setup, find_packages

setup(
    name="propreturns_data_checker_v2",
    version="0.1.0",
    author="Kathan Bhavsar",
    author_email="kathanbhavsar@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "sqlalchemy",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
