# PyScientificStringParser
A python module that converts strings in the metric scientific notation to numerical data types.

This package is available at [PyPI](https://pypi.org/project/scistringparser/).

It is a very simple module that contains one function, made for a specific application, but i think that it can be useful for other people since i couldn't find anywhere a similar package.

## Usage
You can import the module by calling the function `parse_str`.
The input is a string that contains the number in the metric scientific notation, like `1u` -> _1e-6_.

Example:

`parse_str('1.2k')`

Outuput: `1.2e3`

It is compatible with all the metric system prefixes.

## Installation
You can install this package by calling `pip install scistringparser`.