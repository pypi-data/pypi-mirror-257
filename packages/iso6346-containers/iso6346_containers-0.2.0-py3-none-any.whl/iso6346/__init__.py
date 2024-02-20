import re


def normalize(s):
    '''
    Normalise an ISO 6346 owner number for database storage.

    Remove any non-alphanumeric characters and convert to upper-case.
    '''
    return re.sub(r'[^A-Z0-9]', '', s.upper())


def format(s, box=False):
    '''
    Nicely format an ISO 6346 owner number.
    '''
    s = normalize(s)
    if len(s) != 11:
        return s
    if box:
        return f'{s[:4]} {s[4:10]} [{s[10]}]'
    return f'{s[:4]} {s[4:10]} {s[10]}'


def validate(s):
    '''
    Validate ISO 6346 owner number.

    This will validate a given CSC owner number by
    calculating the checkdigit and comparing it against
    the last character in the string.

    All 11 characters exactly must be provided.

    Will return the True if valid.

    Otherwise, will raise a ValueError exception if invalid.
    '''

    # Normalise.
    s = normalize(s)

    # Validate.
    if len(s) != 11:
        raise ValueError('Invalid ISO 6346 container owner number (incorrect length.)')
    d = checkdigit(s)
    e = int(s[10])
    if d != e:
        raise ValueError(f'Invalid ISO 6346 container owner number (checkdigit mismatch: expected {d}; got {e}.)')

    return True


def checkdigit(s):
    '''
    Calculate ISO 6346 checkdigit.

    This will calculate the checkdigit given the first 10 characters
    of a CSC owner number. The 11th character is optional.
    '''

    s = normalize(s)

    # Check string formatting.
    if len(s) < 10 or len(s) > 11:
        raise ValueError('Invalid ISO 6346 container owner number (incorrect length.)')
    if not re.fullmatch(r'^[A-Z]{4}[0-9]{6,7}$', s):
        raise ValueError('Invalid ISO 6346 container owner number (incorrect format.)')

    # Calculate check digit.
    sum = 0
    for i in range(0, 10):
        # Map letters to numbers.
        n = ord(s[i])
        if n < 58:
            n = n - 48
        else:
            n = n - 55

        # Numbers 11, 22, 33 are omitted.
        if n:
            n = n + (n-1) // 10

        # Sum of all numbers multiplied by weighting.
        sum = sum + (n << i)

    # Modulus of 11, and map 10 to 0.
    return (sum % 11) % 10
