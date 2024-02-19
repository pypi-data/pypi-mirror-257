from setuptools import setup, find_packages

def readme():
    with open("README.md", "r") as file:
        return file.read()

setup(
    name="iamstew-excel-parser",
    version="0.0.1",
    author="iamstew",
    author_email="kakylya_ija@bk.ru",
    description="This is module helps to parse xls and xlsx files",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/iamstew/excel-parser",
    packages=find_packages(),
    install_requires=['et-xmlfile>=1.1.0','openpyxl>=3.1.2','xlrd>=2.0.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='xls xlsx excel parser',
    project_urls={
        'GitHub': 'https://github.com/iamstew/excel-parser'
    },
    python_requires=">=3.11.6"
)