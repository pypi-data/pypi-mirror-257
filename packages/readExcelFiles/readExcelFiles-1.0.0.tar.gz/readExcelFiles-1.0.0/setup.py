from setuptools import setup, find_packages

setup(
    name='readExcelFiles',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['xlrd', 'openpyxl', 'pandas', 'xlwings'],  # Add any dependencies here
    author='Harsh Jani',
    author_email='jani99harsh@gmail.com',
    description='A Python package for reading Excel files.',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
