

from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'chiragdemoval'
LONG_DESCRIPTION = 'A package to find area of different figures'


# Setting up
setup(
    name="chiragdemoval",
    version=VERSION,
    author="Chirag",
    author_email="chiragb@quinnox.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
    ],
    keywords=['python', 'tutorial', 'area of figs', 'area'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

# setup(
#     name='demm',
#     version='0.1',
#     packages=find_packages(),
#     license='MIT',
#     author='Chetan',
#     # author_email='chiragb@quinnox.com',
#     description='A short description of your package',
#     long_description=open('README.md').read(),
#     long_description_content_type='text/markdown',
#     url='https://github.com/your_username/your_package_name',
#     install_requires=[
#         'pandas>=1.0.0',
#     ],
#     classifiers=[
#         'License :: OSI Approved :: Your License Name',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: 3.7',
#         'Programming Language :: Python :: 3.8',
#         'Programming Language :: Python :: 3.9',
#     ],
# )




