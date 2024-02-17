from setuptools import find_packages, setup


setup(
    name='pyexplain',
    packages=find_packages(),
    version='0.1.0',
    description='My first Python library',
    author='Me',
    install_requires=[
        'rich',
        'colorama',
        'openai',
        'art'
        ],
    entry_points={
        'console_scripts': [
            'pyexplain-interact = pyexplain.main:main',
            # Add more commands and their corresponding functions
        ],
    },
     classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)