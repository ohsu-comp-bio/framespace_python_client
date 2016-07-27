from setuptools import setup

setup(
    name='framespacer',
    version='0.1.0',
    author='Finn Womack',
    author_email='womackf@ohsu.edu',
    packages=['framespacer'],
    url='https://github.com/ohsu-computational-biology/framespace_r_client',
    license='LICENSE.txt',
    description='A package to help access and manipulate data on the framespace server',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy",
        "json",
        "jsonmerge",
        "requests",
        "pandas"
    ]
)
