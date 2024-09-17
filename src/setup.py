from setuptools import setup, find_packages

setup(
    name='data_metamorphsis',  # Updated package name
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},  # Code in src directory
    install_requires=[],  # Add any required dependencies
    description='A package for the fetching, transforming and visualizing economic & financial data',
    author='Bradley Strong',
    author_email='your.email@example.com',
    url='https://github.com/stochastics/data_metamorphsis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)