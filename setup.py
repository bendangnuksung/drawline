from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='drawline',
    version='0.0.1',
    packages=['drawline'],
    url='https://github.com/bendangnuksung/drawline',
    license='',
    author='bendangnuksung',
    author_email='bendangnuksungimsong@gmail.com',
    description='Clean draw of  rectangle and polygon contours',
    install_requires=required,
    long_description=long_description,
    classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],

)
