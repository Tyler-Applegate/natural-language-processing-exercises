# This is my Data Preparation Module for NLP

# imports
from requests import get
from bs4 import BeautifulSoup
import os
import unicodedata
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

def basic_clean(string):
    '''
    This funtion will take in a single string, 
    - lowercase all of the characters, 
    - normalize unicode characters, 
    - replace anything that is not a letter/number/whitespace/single quote.
    '''
    
    #lowercase all letters in the text
    string = string.lower()
    
    # Normalizaton: Remove inconsistencies in unicode charater encoding.
    # encode the strings into ASCII byte-strings (ignore non-ASCII characters)
    # decode the byte-string back into a string
    string = unicodedata.normalize('NFKD', string)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    
    # remove anything that is not a through z, a number, a single quote, or whitespace
    string = re.sub(r'[^\w\s]', '', string)
    
    return string

def tokenize(string):
    '''
    This function takes in the result of my basic_clean function (a single, cleaned string) and tokenizes all the words in the string.
    It returns the tokenized string as a list
    '''
    
    # Create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()

    # Use the tokenizer
    string = tokenizer.tokenize(string, return_str=True)
    
    return string

def stem(string):
    '''
    This function will take in a single string, perform a PorterStemmer, and return the stemmed string.
    '''
    
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer()
    
    # Apply the stemmer to each word in our string.
    stems = [ps.stem(word) for word in string.split()]
    
    string = ' '.join(stems)

    
    return string

def lemmatize(string):
    '''
    This function will take in a single string, perform lemmatization, and return the lemmatized string.
    '''
    
    
    # Create the Lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Use the lemmatizer on each word in the list of tokenized words.
    lemmas = [wnl.lemmatize(word) for word in string.split()] 
    
    # Join our list of words into a string again; assign to a variable to save changes.
    string = ' '.join(lemmas)
    
    return string

def remove_stopwords(string, extra_words=[], exclude_words=[]):
    '''
    This function will take in a single string ('input_string') that has already been prepped, 
    remove all stop words, and return the string minus the stopwords.
    '''

    # define stopwords
    stopword_list = stopwords.words('english')
    
    # Remove 'exclude_words' from stopword_list to keep in my text.
    stopword_list = set(stopword_list) - set(exclude_words)
    
    # Add 'extra_words' to stopword_list
    stopword_list = stopword_list.union(set(extra_words))
    
    # split words in string
    words = string.split()
        
    # create a list of words from my string with stopwords removed
    filtered_words = [word for word in words if word not in stopword_list]
    
    # join words in list back into strings
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords


def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    df[f'cleaned_{column}'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    df[f'stemmed_{column}'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(stem)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    df[f'lemmatized_{column}'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(lemmatize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    return df

