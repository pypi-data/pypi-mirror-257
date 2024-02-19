from setuptools import setup, find_packages

setup(
    name = "privyml",
    version = "0.0.1",
    packages=find_packages(),
    requires=['torch','cryptography','skimage','numpy','os','csv','io','uuid'],
)