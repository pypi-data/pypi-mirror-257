from setuptools import setup, find_packages

setup(
    name='gravpy-core',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy'
    ],
    author='javi22020',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)