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

########################### For a Single Article ###########################

def get_article(article, category):
    '''
    This function takes in a single article and category, and returns a dictionary with the
    article 'title', 'content', and 'category'.
    '''
    # Attribute selector (grabbing the title)
    title = article.select("[itemprop='headline']")[0].text
    
    # article body (grabbing the content)
    content = article.select("[itemprop='articleBody']")[0].text
    
    # create the empty dictionary
    output = {}
    
    # add each variable to the dictionary
    output["title"] = title
    output["content"] = content
    output["category"] = category
    
    return output

######################## For a List of Articles within 1 Category #############################

def get_articles(category, base ="https://inshorts.com/en/read/"):
    """
    This function takes in a category as a string. Category must be an available category in inshorts
    Returns a list of dictionaries where each dictionary represents a single inshort article
    """
    
    # We concatenate our base_url with the category
    url = base + category
    
    # Set the headers
    headers = {'User-Agent': 'Codeup Data Science'}

    # Get the http response object from the server
    response = get(url, headers=headers)

    # Make soup out of the raw html
    soup = BeautifulSoup(response.text)
    
    # Ignore everything, focusing only on the news cards
    articles = soup.select(".news-card")
    
    # create an empty list
    output = []
    
    # Iterate through every article tag/soup 
    for article in articles:
        
        # Returns a dictionary of the article's title, body, and category
        article_data = get_article(article, category) 
        
        # Append the dictionary to the list
        output.append(article_data)
    
    # Return the list of dictionaries
    return output

####################### For All Articles in All Categories #############################

def get_all_news_articles(categories):
    """
    Takes in a list of categories where the category is part of the URL pattern on inshorts
    Returns a dataframe of every article from every category listed
    Each row in the dataframe is a single article
    """
    # Create a list for all inshorts articles
    all_inshorts = []
    
    # loop through each category
    for category in categories:
        # grab each article from a particular category
        all_category_articles = get_articles(category)
        # add each list of articles/category to the all_inshorts list
        all_inshorts = all_inshorts + all_category_articles

    # make it a dataframe
    df = pd.DataFrame(all_inshorts)
    return df