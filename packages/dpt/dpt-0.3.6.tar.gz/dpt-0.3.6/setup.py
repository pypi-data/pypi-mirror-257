from setuptools import setup, find_packages

name = "dpt"
packages = [pkg for pkg in find_packages() if pkg.startswith(name)]

setup(
    name=name,
    version="0.3.6",
    author="DF",
    author_email="your_email@example.com",
    packages=packages,
    install_requires=[
        "GitPython>=3.1.41",
        "pymongo>=4.6.1",
        "jsonschema>=4.6.0",
        "pydantic==2.5.3",
        "uvicorn==0.27.0",
        "fastapi==0.109.0",
        "pyparsing==3.1.1",
        "requests==2.31.0",
    ],
)
