import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="readmepp",
    version="0.0.1",
    author="Tarek Naous",
    author_email="tareknaous@gmail.com",
    description="BERT models for readability prediction in multiple languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tareknaous/readme",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)