import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sportsdata-koverstreet",
    version="0.0.1",
    author="Kyle Overstreet",
    author_email="koverstreet@gmail.com",
    description="An API for retrieving sports data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kyle1/sportsdata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)