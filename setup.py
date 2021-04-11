import setuptools
from histogrammer import __version__
print(__version__)

install_requires = [
    "root_pandas>=0.7.0",
    "numpy",
    "pandas"
]

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="histogrammer-pkg", # Replace with your own username
    version=__version__,
    author="S. Bilokin",
    author_email="belle2@desy.de",
    description="A package that plots histograms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires
)
