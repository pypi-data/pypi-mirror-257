import re


def checksum(s):
    '''
    Calculate ISO 6346 checksum.
    '''

    # Remove any non-alphanumeric characters and convert to upper-case.
    s = re.sub(r'[^A-Z0-9]', '', s.upper())

    # Check if length fits requirements.
    if len(s) < 10 or len(s) > 11:
        raise ValueError('Invalid ISO 6346 container owner number (incorrect length.)')

    # Calculate check digit.
    sum = 0
    for i in range(0, 10):

        # Map letters to numbers.
        n = ord(s[i])
        #n = n - n < 58 ? 48 : 55;
        n = n - 48 if n < 58 else 55

        # Numbers 11, 22, 33 are omitted.
        n = n + (n-1) // 10

        # Sum of all numbers multiplied by weighting.
        sum = sum + n << i

    # Modulus of 11, and map 10 to 0.
    sum = sum % 11 % 10
    return sum


def validate(s):
    pass


def format(s):
    pass
