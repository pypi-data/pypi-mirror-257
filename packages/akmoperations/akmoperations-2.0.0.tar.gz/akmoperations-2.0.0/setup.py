from setuptools import setup, find_packages

setup(
    name='akmoperations',
    version='2.0.0',  # Update the version as needed
    author='akm',
    author_email='akm@gmail.com',
    description='AKM Operations Package',
    long_description='A simple Python package for addition with unit tests.',
    url='https://github.com/vishal-meshram/akmaddition.git',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)