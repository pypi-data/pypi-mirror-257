from setuptools import setup, find_packages

setup(
    name='brushtail',
    version='0.0.2',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'requests',
        'selenium',
        'beautifulsoup4'
    ],
    author='Ethan Vellacott',
    description='A small python framework for making simple, maintainable web scraping scripts.',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EthanVellacott/brushtail',
    python_requires='>=3.11',
)
