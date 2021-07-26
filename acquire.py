# This is my Data Acquisition Module for NLP

# imports
import requests
from requests import get
from bs4 import BeautifulSoup
import os

################ Fancy Functions to Blog About ##################################

def get_title_content(url):
    '''
    This function will take in a single url as a string, create an empty dictionary. It will return a dictionary with the 'title' of the article, and 'content' of the article.
    '''
    # create empty dictionary
    blog_dict = {}
    
    # the header tells the website who is pulling the data
    headers = {'User-Agent': 'Codeup Data Science'}
    
    # response is 'get'ting the data from the website
    response = get(url, headers=headers)
    
    # make that delicious Campbells (return the text)
    soup = BeautifulSoup(response.text)
    
    # give me the entire content as text
    content = soup.find('div', class_='jupiterx-post-content')
    
    # give me the title as text
    title = soup.find('h1', class_='jupiterx-post-title')
    
    # add title and content to dictionary
    blog_dict = {'title': title.text,
                'content': content.text}

    return blog_dict

def get_blog_articles(url_list):
    '''
    This function takes in a list of URLs from the Codeup blog, and returns a dictionary of each articles 'title' and content'
    '''
    
    # create an empty ist
    list_of_blogs = []
    
    # cycle through each url in the list
    for url in url_list:
        # call on the 'get_title_content' function to create a dictionary for each url
        # append each dictionary
        list_of_blogs.append(get_title_content(url))
        
    return list_of_blogs