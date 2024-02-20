# ISO 6346 Freight Containers: Coding, Identification and Marking

[API Documentation](https://iso6346-containers.readthedocs.io/en/latest/)

## Synopsis

CSC owner codes.

The calculation is based upon:

 * [How is the check digit of a container calculated? — Grand View Container Trading](http://www.gvct.co.uk/2011/09/how-is-the-check-digit-of-a-container-calculated/)
 * [ISO 6346:2022 Freight containers — Coding, identification and marking](https://www.iso.org/standard/83558.html)

## Installation

See the PyPI package [`iso6346-containers`](https://pypi.org/project/iso6346-containers/):

```
pip install iso6346-containers
```

### Example

```
>>> import iso6346
>>> iso6346.format('CHEG1231232')
'CHEG 123123 2'
>>> iso6346.format('CHEG1231232', box=True)
'CHEG 123123 [2]'
>>> iso6346.normalize('CHEG 123123 [2]')
'CHEG1231232'
>>> iso6346.checkdigit('CHEG1231232')
2
>>> iso6346.validate('CHEG1231232')
True
>>> iso6346.validate('CHEG1231238')
Traceback (most recent call last):
  File "<console>", line 1, in <module>
    File "/home/dbezborodov/src/iso6346py/src/iso6346/__init__.py", line 46, in validate
        raise ValueError(f'Invalid ISO 6346 container owner number (checkdigit mismatch: expected {d}; got {e}.)')
        ValueError: Invalid ISO 6346 container owner number (checkdigit mismatch: expected 2; got 8.)
```

## See Also

 * [`langerheiko/Calc-ILU-check-digit`](https://github.com/langerheiko/Calc-ILU-check-digit) _(JavaScript)_

### Example

```
>>> import iso6346
>>> iso6346.format('CHEG1231232')
'CHEG 123123 2'
>>> iso6346.format('CHEG1231232', box=True)
'CHEG 123123 [2]'
>>> iso6346.normalize('CHEG 123123 [2]')
'CHEG1231232'
>>> iso6346.checkdigit('CHEG1231232')
2
>>> iso6346.validate('CHEG1231232')
True
>>> iso6346.validate('CHEG1231238')
Traceback (most recent call last):
  File "<console>", line 1, in <module>
    File "/home/dbezborodov/src/iso6346py/src/iso6346/__init__.py", line 46, in validate
        raise ValueError(f'Invalid ISO 6346 container owner number (checkdigit mismatch: expected {d}; got {e}.)')
        ValueError: Invalid ISO 6346 container owner number (checkdigit mismatch: expected 2; got 8.)
```

## Author

2024 Damien Bezborodov
