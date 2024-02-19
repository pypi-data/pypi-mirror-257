from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="immpy",
    version="2.2.1",
    description="A package for the management of patterns in indoor mobility data",
    long_description=readme(),
    long_description_content_type="Functions implemented: Stop_Detection, Nearest_Poi_Detection, Visit_Detection",
    author="Ip2211po",
    author_email="ip2211po@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        'pandas',
        'prettytable',
        'scipy',
        'matplotlib'
    ],
    packages=["immpy"],
    include_package_data=True,
)