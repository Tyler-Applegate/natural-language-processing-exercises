# This is my Data Preparation Module for NLP

# imports
from requests import get
from bs4 import BeautifulSoup
import os



def basic_clean(original):
    '''
    This funtion will take in a single string, 
    - lowercase all of the characters, 
    - normalize unicode characters, 
    - replace anything that is not a letter/number/whitespace/single quote.
    '''
    
    #lowercase all letters in the text
    article = original.lower()
    
    # Normalizaton: Remove inconsistencies in unicode charater encoding.
    # encode the strings into ASCII byte-strings (ignore non-ASCII characters)
    # decode the byte-string back into a string
    article = unicodedata.normalize('NFKD', article)\
    .encode('ascii', 'ignore')\
    .decode('utf-8')
    
    # remove anything that is not a through z, a number, a single quote, or whitespace
    article = re.sub(r"[^a-z0-9'\s]", '', article)
    
    return article

def tokenize(prepped_article):
    '''
    This function takes in the result of my basic_clean function (a single, cleaned string) and tokenizes all the words in the string.
    It returns the tokenized string as a list
    '''
    
    # Create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()

    # Use the tokenizer
    tokenized_article = tokenizer.tokenize(prepped_article)
    
    return tokenized_article

def stem(tokenized_article):
    '''
    This function will take in a single string, perform a PorterStemmer, and return the stemmed string.
        
    *** This function is set up to run AFTER using the 'tokenize' function. ***
    If the 'tokenize' function has not been called, then we need to use a .split() in the for loop.
    '''
    
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer()
    
    # Apply the stemmer to each word in our string.
    stems = [ps.stem(word) for word in tokenized_article] # Need to add .split() after tokenized_article if tokenization has not occured
    
    article_stemmed = ' '.join(stems)

    
    return article_stemmed

def lemmatize(tokenized_article):
    '''
    This function will take in a single string, perform lemmatization, and return the lemmatized string.
    
    *** This function is set up to run AFTER using the 'tokenize' function. ***
    If the 'tokenize' function has not been called, then we need to use a .split() in the for loop.
    '''
    
    
    # Create the Lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Use the lemmatizer on each word in the list of tokenized words.
    lemmas = [wnl.lemmatize(word) for word in tokenized_article] # Need to add .split() after tokenized_article if tokenization has not occured
    
    
    # Join our list of words into a string again; assign to a variable to save changes.
    article_lemmatized = ' '.join(lemmas)
    
    return article_lemmatized

def remove_stopwords(input_string, extra_words=None, exclude_words=None):
    '''
    This function will take in a single string ('input_string') that has already been prepped, remove all stop words, and return the string minus the stopwords.
    - [extra_words] = list of additional words to add to stopword_list; default=None
    - [exclude_words] = list of words to remove from stopword_list, and leave in 'output_string'; default=None
    - each list must be defined outside of the function
    - *** if 'input_string' has not been lemmatized, will need to do so before function can run properly.
    '''
    
    # lemmatize if necessary
#     words = lemmatize(input_string).split()

    # if 'input_string' already lemmatized,
    words = input_string.split()
    
    # define stopwords
    stopword_list = stopwords.words('english')
    
    if extra_words == None:
        stopword_list = stopword_list
        
    else:
        for word in extra_words:
            stopword_list.append(word)
            
    if exclude_words == None:
        stopword_list = stopword_list
    else:
        for word in exclude_words:
            stopword_list.remove(word)
        
    # create a list of words from my string with stopwords removed
    filtered_words = [word for word in words if word not in stopword_list]
    
    # join words in list back into strings
    article_without_stopwords = ' '.join(filtered_words)
    
    return article_without_stopwords


