from setuptools import setup , find_packages

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
    install_requires=[
        'markdown'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
