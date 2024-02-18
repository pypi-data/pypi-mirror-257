from setuptools import setup, find_packages

setup(
    name='keliya_lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    author='Erandra Jayasundara',
    author_email='erandraj@gmail.com',
    description='AWS Lambda helpers',
    license='MIT'
)
