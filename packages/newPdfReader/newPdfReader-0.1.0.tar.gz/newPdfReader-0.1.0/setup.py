from setuptools import setup, find_packages

setup(
    name='newPdfReader',
    version='0.1.0',
    description='A utility for reading text from PDF files',
    long_description='A Python library for extracting text from PDF files using PyMuPDF (fitz)',
    author='jayesh vani',
    author_email='jayeshvani2@gmail.com',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF>=1.18.15',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
