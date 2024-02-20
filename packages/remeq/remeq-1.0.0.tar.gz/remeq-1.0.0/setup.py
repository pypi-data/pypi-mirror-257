from setuptools import find_packages, setup

with open("remeq/README.md", "r") as f:
    long_description = f.read()

setup(
    name="remeq",
    version="1.0.0",
    description="A simple library for creating message queue based on Redis and its channels",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndrewLt/remeq",
    author="AndrewLt",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    keywords=['redis', 'queue', 'message'],
    install_requires=[
        "redis>=5.0.0",
        "hiredis"
    ],
    python_requires=">=3.9",
)
