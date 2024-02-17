from setuptools import setup, find_packages

setup(
    name='lindle',
    version='1.0.0',
    author='M2K Developments',
    author_email='m2kdevelopments@gmail.com',
    description='Lindle Python API saving tool to keep all your links all in one place',
    long_description=open('README.md').read()+'\n\n'+open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url='https://lindle.me',
    packages=find_packages(),
    keywords='lindle links bookmarks',
    license='MIT',
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)