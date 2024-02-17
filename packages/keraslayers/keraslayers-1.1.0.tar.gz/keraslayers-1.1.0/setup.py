from setuptools import setup, find_packages

setup(
    name='keraslayers',
    version='1.1.0',
    packages=find_packages(),
    author='',
    author_email='',
    description='Keras models and utilities',
    license='MIT', 
    install_requires=[
        'numpy',
        'tensorflow',
        'keras',
        'pandas', 
        'cloudscraper',
        'requests',
        'beautifulsoup4',
        'keras',
    ]
)
