
from setuptools import setup, find_packages

setup(
    name='ElegooSmartCarController',
    version='0.1.0',
    packages=find_packages(),
    description='A Python library to control Elegoo Smart Car V4',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Frederick Feraco',
    author_email='frederick.feraco@gmail.com',
    url='https://github.com/yourgithub/ElegooSmartCarController',  # Replace with your actual GitHub URL
    install_requires=[],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
