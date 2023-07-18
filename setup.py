from setuptools import setup, find_packages

setup(
    name='gdrive3',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'pydrive2',
        'appdirs',
        'fsspec',
        'pandas',
        'funcy',
        'tqdm',
        'joblib',
    ],
    entry_points={
        'console_scripts': [

        ],
    },
    author='Charlie Sergeant',
    author_email='sergeach@kean.edu',
    description='Google Drive as blob storage - an extension of PyDrive2',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CharlieSergeant/gdrive3',
    license='MIT',  # Choose an appropriate license for your package
)