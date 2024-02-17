from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A library to make quaternion neural networks.'

with open("README.md") as fh: LONG_DESCRIPTION = fh.read()

# Setting up
setup(
    name="qytorch",
    version=VERSION,
    author="smlab-niser",
    author_email="smishra@niser.ac.in",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/smlab-niser/qytorch",
    packages=find_packages(),
    install_requires=[
        'torch',
        # 
    ],
    keywords=['quaternion', 'neural networks', 'torch', 'machine learning', 'parameter reduction'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        
    ]
)
