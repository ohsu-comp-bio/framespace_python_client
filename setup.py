from setuptools import setup

setup(
    name='framespace',
    version='0.1.0',
    author='Finn Womack, Alex Buchanan',
    author_email='womackf@ohsu.edu, buchanae@ohsu.edu',
    packages=['framespace'],
    url='https://github.com/ohsu-computational-biology/framespace_python_client',
    license='LICENSE.txt',
    description='Client library to help access and manipulate data on the framespace server',
    long_description=open('README.md').read(),
    install_requires=[
        "protobuf",
        "requests",
    ]
)
