# Scheme interpreter in python

This project is a work in progress. Many features are missing. I am putting
things together piece by piece

## Introduction
A subset of features for the
[R5RS](https://schemers.org/Documents/Standards/R5RS)
[Scheme](https://en.wikipedia.org/wiki/Scheme_(programming_language))
implemented in python as a learning project. The only dependency is a recent
python version (tested with python >= 3.7)

## Architecture
This is generic tree walking interpreter:<br>

```
Source Code ---> Parser ---> Abstract Syntax Tree ---> Evaluater ---> Result
```

## Usage
To run:
```
python3 main.py
```
This will launch a REPL. To interpret a file:
```
python3 main.py <filename>
```

To run tests:
```
python3 -m unittest discover
```
[unittest](https://docs.python.org/3/library/unittest.html) was used because it
is available by default

## Inspiration
http://norvig.com/lispy.html

## License
[Public domain](https://unlicense.org) or
[MIT](https://opensource.org/licenses/MIT) at your option
