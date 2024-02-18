from setuptools import setup, find_packages

setup(
    name="chinese-nonwords",
    version="0.1.0",
    author="Mingyu Yuan",
    author_email="",
    description="A package for generating Chinese disyllabic nonwords",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
