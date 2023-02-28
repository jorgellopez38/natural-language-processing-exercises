import pandas as pd
import numpy as np
from requests import get
from bs4 import BeautifulSoup
import os
import json



################################################ Acquire Codeup Blog Function ################################################

def get_blog_articles(article_list):
    
    file = 'blog_posts.json'
    
    if os.path.exists(file):
        
        with open(file) as f:
            
            return json.load(f)
        
    headers = {'User-Agent': 'Codeup Data Science'}
    # create empty list
    article_info = []
    # for loop
    for article in article_list:
        
        response = get(article, headers=headers)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # make dictionary
        info_dict = {'title': soup.find('h1').text,
                     'link': link,
                     'date_published': soup.find('span', class_='published').text,
                     'content': soup.find('div', class_='entry-content').text
                    }
        # append it
        article_info.append(info_dict)
        
    with open(file, 'w') as f:
        
        json.dump(article_info, f)
        
    return article_info


################################################ Acquire Inshorts Blog Function 1 ################################################


def scrape_one_page(topic):
    
    base_url = 'https:inshorts.com/en/read/'
    
    response = get(base_url + topic)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    titles = soup.find_all('span', itemprop='headline')
    
    summaries = soup.find_all('div', itemprop='articleBody')
    
    summary_list = []
    
    for i in range(len(titles)):
        
        temp_dict = {'category': topic,
                     'title': titles[i].text,
                    'content': summaries[i].text
                    }
        
        summary_list.append(temp_dict)
    
    return summary_list


################################################ Acquire Inshorts Blog Function 2 ################################################


# define a function that will scrape information about an array of topics
def get_news_articles(topic_list):
    
    file = 'news_articles.json'
    
    if os.path.exists(file):
        
        with open(file) as f:
            
            return json.load(f)
    
    final_list = []
    
    for topic in topic_list:
        
        final_list.extend(scrape_one_page(topic))
        
    with open(file, 'w') as f:
        
        json.dump(final_list, f)
    
    return final_list

