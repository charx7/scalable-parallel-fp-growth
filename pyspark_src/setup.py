from setuptools import setup , find_packages

# Parse the requirements form a requirements.txt file
def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

# Call the function
requirements = parse_requirements('requirements.txt')

with open("README.md", "r") as fh:
   long_description = fh.read()
# long_description = "This is a long description of my pkg"

setup(
    name="pyspark_recom_engine",
    version="0.1",
    author="Charx, Michael, Ankit",
    author_email="carlos.huertaso@udlap.mx",
    description="Recommendation engine using spark",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="tbd",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
