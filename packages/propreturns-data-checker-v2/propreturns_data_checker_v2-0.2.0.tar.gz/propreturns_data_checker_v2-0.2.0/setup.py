from setuptools import setup, find_packages

setup(
    name="propreturns_data_checker_v2",
    version="0.2.0",
    author="Kathan Bhavsar",
    author_email="kathanbhavsar@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "sqlalchemy",
        "click",  # Adding click as a dependency for the CLI tool
    ],
    entry_points={
        "console_scripts": [
            "propreturns_configure_tool=propreturns_data_checker.cli_tool:configure_tool",
        ],
    },
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
