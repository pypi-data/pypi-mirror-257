from setuptools import setup
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='daawoud',
    version='1.0',
    author='Ahmed Hamdi',
    description='A Colorings and Centering text library made by Ahmed Hamdi',
    packages=setuptools.find_packages(),
    keywords=['daawoud-lib library', 'coloring python', 'python colors', 'daawoud-lib', 'ahmed hamdi', 'center text python'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    py_modules=['daawoud-lib'],
    package_dir={'':'src'},
    install_requires = [
        'colorama'
    ]
)
