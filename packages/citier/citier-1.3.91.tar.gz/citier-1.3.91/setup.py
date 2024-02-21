from setuptools import setup, find_packages

with open('citier/README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='citier',
    version='1.3.91',
    packages=find_packages(),
    install_requires=[],
    entry_points={},
    description='An extensive Python Library to View, List and Validate Countries, States, and Cities data',
    long_description= long_description,
    long_description_content_type='text/markdown',
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
