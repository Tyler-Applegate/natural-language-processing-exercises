# These are my initial regex functions for Natural Language Processing

# imports
import pandas as pd
import re

def is_vowel(subject):
    '''
    This function will take in a string and look for an exact match for a single character vowel. It will return a boolean value.
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

def extract_lines(target):
    '''
    This function takes in a string of logfiles. It creates an empty pandas DataFrame. 
    Creates an 'input_line' column that splits the original string by line, and returns the original input.
    Finally, it extracts the following sections of the original line, and returns a new column for each:
    - method
    - path
    - timestamp
    - status
    - bytes_sent
    - user_agent
    - ip
    '''
    
    # (?P<method>[A-Z]+) = begins with 1 or more cap letters, stored as 'method'
    # \s = separated by whitespace
    # (?P<path>.*) = 'path' could be any character(s) of any length
    # \s = separated by whitespace
    # HTTP/1.1 = literall HTTP/1.1
    # \s = separated by whitespace
    # {(?P<status>\d+)} = 'status' of 1 or more non-digit characters
    # \s = separated by whitespace
    # (?P<bytes_sent>\d+) = 'bytes_sent' of 1 or more digit characters
    # \s = separated by whitespace
    # "(?P<user_agent>.*)" = 'user_agent' inside "" of any character(s) zero or more times
    # \s = separated by whitespace 1 or more times
    # (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) = 'ip' of 1 to 3 digits, '.' 4x


    
    regexp = r'''
(?P<method>[A-Z]+)
\s
(?P<path>.*)
\s
\[(?P<timestamp>.*)\]
\s
HTTP/1.1
\s
{(?P<status>\d+)}
\s
(?P<bytes_sent>\d+)
\s
"(?P<user_agent>.*)"
\s+
(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
'''
    # compiles the VERBOSE regexp
    regexp = re.compile(regexp, re.VERBOSE)
    
    # creates empty pandas DataFrame
    df = pd.DataFrame()
    
    # creates 'input_line' column of original data
    df['input_line'] = lines.strip().split('\n')
    
    # concatenates 'input_line' and the extracted regexp data
    df = pd.concat([df, df['input_line'].str.extract(regexp)], axis=1)
    
    return df

def get_words():
    '''
    This function looks for a locally stored list of words. It read them in, drops nulls, 
    and converts all characters to lowercase. Returns a pandas Series.
    '''
    # reads in the locally stored list of words, and drops null values
    words = pd.read_csv('/usr/share/dict/words', header=None, squeeze=True).dropna()
    
    # converts all characters to lowercase
    words = words.str.lower()
    
    return words

def more_vowels(target_list):
    '''
    This function takes in a pandas Series in an attempt to determine if each string has more vowels.
    First, we create an empty pandas DataFrame. Then an 'input_data' column that contains the target_list.
    A 'vowel_count' column is created that has a sum of each strings vowel count.
    A 'cons_count' column is created that has a sum of each strings consonant count.
    A 'mas_vowels' column is created that holds a boolean value of whether or not the string has more vowels than consonants.
    Finally, an update pandas DataFrame, along with a total count are returned.
    '''
    
    # make an empty DataFrame
    df = pd.DataFrame()
    
    # create input data column
    df['input_data'] = words
    
    # create vowel count column
    df['vowel_count'] = words.str.count(r'[aeiou]')
    
    # create consonant count column
    df['cons_count'] = words.str.count(r'[^aeiou]')
    
    # create a more vowels column
    df['mas_vowels'] = df['vowel_count'] > df['cons_count']
    
    # assign a variable to the sum of strings with more vowels than consonants
    target_count = df['mas_vowels'].sum()
    
    return df, target_count
