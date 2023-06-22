from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="simple_arn",
    description="simple AWS arn parsing and serialization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eric Austin",
    url="https://github.com/ericmaustin/aws_arn",
    license="MIT",
    author_email="eric.m.austin@gmail.com",
    python_requires=">=3.7",
    version="0.0.2",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[]
)