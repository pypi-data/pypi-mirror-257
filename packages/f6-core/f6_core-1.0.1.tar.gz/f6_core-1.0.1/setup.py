from setuptools import setup, find_packages
from os.path import abspath, dirname, join

README_MD = open(join(dirname(abspath(__file__)), "README.md")).read()

setup(
    name="f6_core",
    version="1.0.1",
    packages=find_packages(exclude="tests"),
    description="""The "F6" program is a program designed to work with electronic
     paper accounting of attendance and academic performance of students of secondary professional
     organizations, which generates reports in the form of an extract – "Form 6".""",
    long_description=README_MD,
    long_description_content_type="text/markdown",
    url="",
    # author_name="Ivan Degtyarev",
    # author_email="",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only"
    ],
    keywords="f6, f6_core",

)