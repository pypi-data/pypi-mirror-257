from setuptools import setup, find_packages

setup(
    name='scistringparser',
    version='0.1.0',
    description='A python module that converts strings in the metric \
    scientific notation to numerical data types.',
    author='Rodrigo Moraes',
    author_email='rodrigo.smoraes98@gmail.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)