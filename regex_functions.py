# These are my initial regex functions for Natural Language Processing

# imports
import pandas as pd
import re

def is_vowel(subject):
    '''
    This function will take in a string and look for an exact match for a single character vowel. 
    It will return a boolean value.
    '''
    
    # startswith an upper or lowercase vowel, and is only 1 character
    regexp = r'^[aeiouAEIOU]$'
    
    vowel = re.search(regexp, subject)
    
    return bool(vowel)

def is_valid_username(subject):
    '''
    This function accepts a username as a string and returns a boolean value based on whether or not the username meets the following requirements: 
    - starts with a lowercase letter
    - only consists of lowercase letter, numbers, or the '_' character
    - no longer than 32 characters
    '''
    
    # ^[a-z] = starts with a lowercase letter
    # [a-z0-9_]{,31}$ = followed by any combination of lowercase letters, numbers, or underscores up to 31 characters in length
    regexp = r'^[a-z][a-z0-9_]{,31}$'
    
    username = re.search(regexp, subject)
    
    return bool(username)

def capture_phone_numbers(target):
    '''
    This function takes in a pandas Series of phone numbers, creates a pandas DataFrame with one col:
    - may start with '+', '(' or any digit
    - may be 8 to 15 characters
    - may contain whitespace
    '''
    
    # Create a blank dataframe
    df = pd.DataFrame()
    
    # assign the target variable list to a column in the df
    df['input_number'] = target
    
    # create the regexp to compile the sections of the phone numbers
    phone_regex = re.compile(
                            '''
                            ^ 
                            (?P<country_code>\+\d+)?
                            \D*?
                            (?P<area_code>\d{3})?
                            \D*?
                            (?P<exchange_code>\d{3})
                            \D*?
                            (?P<line_number>\d{4})
                            \D*
                            $
                            ''', re.VERBOSE)
    
    # Output results to the dataframe
    df = df['input_number'].str.extract(phone_regex)
    
    # creates a column with the original input
    df['input_number'] = target
    
    return df


def convert_date_format(target):
    '''
    This function takes in a pandas Series. It creates an empty pandas DataFrame. Creates a column of the original input_date that is in MM/DD/YY format. It then converts that format to YYYY-MM-DD and returns a 'converted_date' column. This new column is then converted to datetime. Finally, the entire DataFrame is returned with the original input date, and the converted datetime format as well.
    '''
    
    # Create a blank dataframe
    df = pd.DataFrame()
    
    # assign the target variable list to a column in the df
    df['input_date'] = target
        
    # create the regexp to compile the sections of the phone numbers
    date_regexp = r'(\d+)/(\d+)/(\d+)'

    # create output format
    output = r'20\3-\1-\2'
        
    # create new column of converted dates
    df['converted_date'] = [re.sub(date_regexp, output, i) for i in target]
    
    # convert to datetime
    df['converted_date'] = pd.to_datetime(df['converted_date'])
    
    return df