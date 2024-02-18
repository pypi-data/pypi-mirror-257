from setuptools import setup, find_packages

setup(
    name='scistringparser',
    version='0.1.4',
    description='A python module that converts strings in the metric scientific notation to numerical data types.',
    long_description=open("README.md", 'r').read(),
    long_description_content_type='text/markdown',
    author='Rodrigo Moraes',
    author_email='rodrigo.smoraes98@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/RodrigoMoraes98/PyScientificStringParser',
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)