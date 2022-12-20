# Scheme interpreter in python

## Introduction
A subset of features for the
[R5RS](https://schemers.org/Documents/Standards/R5RS)
[Scheme](https://en.wikipedia.org/wiki/Scheme_(programming_language))
implemented in python as a learning project. The only dependency is python
version >= 3.8

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
