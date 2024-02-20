from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r', encoding="utf-8") as f:
    return f.read()
    
setup(name='polars_partitions',
    version='0.1.1',
    author='denis_lvov',
    author_email='dwenlvov@gmail.com',
    description='Simplified work with partitions based on Polars library',
    packages=find_packages(),
    url='https://github.com/dwenlvov/',
    project_urls={
        'Documentation': 'https://github.com/dwenlvov/polars_partitions'
        },
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License'
        ],
    keywords='polars, partitions, parquet',
    python_requires='>=3.11'
    )
