from setuptools import setup, find_packages

setup(
    name='bitheap_gateway_client',
    version='0.1.0',
    author='Your Name',
    author_email='laurentiu@bitheap.tech',
    packages=find_packages(),
    description='A Bitcoin gateway client for generating QR codes for payments in shops',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LaurentiuGabriel/bitheap-gateway-python-client',
    install_requires=[
        'requests',
    ],
)