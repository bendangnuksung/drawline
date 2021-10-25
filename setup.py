from setuptools import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='drawline',
    version='0.3.1',
    packages=['drawline'],
    url='https://github.com/bendangnuksung/drawline',
    license='MIT License',
    author='bendangnuksung',
    author_email='bendangnuksungimsong@gmail.com',
    description='Clean draw of  rectangle and polygon contours',
    install_requires=required,
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],

)
