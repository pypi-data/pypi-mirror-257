from __future__ import annotations

from pathlib import Path

from setuptools import find_packages
from setuptools import setup

# Get base working directory.
base_dir = Path(__file__).resolve().parent

# Readme text for long description
with open(base_dir / 'README.md') as f:
    readme = f.read()

setup(
    name='errant-prep',
    version='v1.0.0rc05',
    license='MIT',
    description='The ERRor ANnotation Toolkit (ERRANT). \
        Automatically extract and classify edits in parallel sentences.',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords=[
        'automatic annotation',
        'grammatical errors',
        'natural language processing',
    ],
    python_requires='>= 3.9',
    install_requires=['spacy>=3', 'rapidfuzz>=2.0.0'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'errant_compare = errant.cli.compare_m2:main',
            'errant_m2 = errant.cli.m2_to_m2:main',
            'errant_parallel = errant.cli.parallel_to_m2:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
)
