from setuptools import setup, find_packages

setup(
    name="mzlogging",
    version="1.5.1",
    author='Zardin Nicolo',
    description='A logging package for Python. It provides a simple way to log messages to console, file and database.',
    packages=find_packages(exclude=['tests*', 'tests']),
    install_requires=[
        "mysql-connector-python",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
