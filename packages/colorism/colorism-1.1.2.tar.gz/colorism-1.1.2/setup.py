from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='colorism',
    version='1.1.2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description='A Python package for color formatting in the terminal.',
    author='federikowsky',
    license='MIT',
    url='https://github.com/federikowsky/Colorism',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        # List any dependencies your package may have
    ],
)
