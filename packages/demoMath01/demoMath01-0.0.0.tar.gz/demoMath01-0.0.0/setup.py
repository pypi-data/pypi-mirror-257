from setuptools import setup, find_packages

setup(
    name="demoMath01",
    version="0.0.0",
    author="Sanyam Gupta",
    author_email="sanyam233@gmail.com",
    description="demo add and subtract functions",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["demoMath01 = src.main"]},
)