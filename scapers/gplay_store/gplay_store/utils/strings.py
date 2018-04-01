import re

def app_size_string_to_float(s):
    number = s.split('M')[0]
    return float(number)
