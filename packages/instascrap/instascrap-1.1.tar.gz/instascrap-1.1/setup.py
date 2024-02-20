from setuptools import setup


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='instascrap',
    version='1.1',
    packages=['instascrap'],
    install_requires=['apify-client'],
    description='nstascrap is a Python module for scraping Instagram profile data.',
    author='Yousseif Muhammed',
    author_email='me@usif.tech',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
