# This is my Data Acquisition Module for NLP
# Codeup Blog Articles

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
    

#################### Functions from curriculum ##################################

def get_article_text():
    '''
    
    '''
    # if we already have the data, read it locally
    if os.path.exists('article.txt'):
        with open('article.txt') as f:
            return f.read()

    # otherwise go fetch the data
    url = 'https://codeup.com/codeups-data-science-career-accelerator-is-here/'
    # This tells the website that I am 'Codeup Data Science'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    article = soup.find('div', class_='jupiterx-post-content')

    # save it for next time
    with open('article.txt', 'w') as f:
        f.write(article.text)

    return article.text



