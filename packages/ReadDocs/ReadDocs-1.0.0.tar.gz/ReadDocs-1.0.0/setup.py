from setuptools import setup, find_packages

setup(
    name='ReadDocs',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['PyMuPDF'],
    author='Jayesh vani',
    author_email='jayeshvani2@gmail.com',
    description='A Python package for extracting text from PDF files.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
