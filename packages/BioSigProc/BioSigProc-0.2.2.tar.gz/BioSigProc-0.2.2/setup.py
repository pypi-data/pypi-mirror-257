from setuptools import setup, find_packages

# Read the content of README.md
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='BioSigProc',
    version='0.2.2',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
        'numpy',
        'matplotlib',
        "PyWavelets",
        # Add more as needed
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Guillaume Francois Deside',
    author_email='guillaume.deside28@gmail.com',
    description='A package for processing and analyzing biomedical signals.',
    url='https://github.com/gdeside/BioSigProc',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    license="Apache Software License 2.0"
)
