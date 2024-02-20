from setuptools import setup, find_packages

setup(
    name='ReadPdfFiles',
    version='1.0.1',
    packages=find_packages(),
    install_requires=['PyMuPDF', 'PyPDF2', 'tabula-py', 'pdfminer.six'],  # Add any dependencies here
    author='Jayesh Vani',
    author_email='jayeshvani2@gmail.com',
    description='A Python package for reading PDF files.',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
