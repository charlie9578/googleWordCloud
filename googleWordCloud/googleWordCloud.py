#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 18:22:59 2020

Helper functions

@author: charlie
"""



from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time
import sys
from wordcloud import WordCloud, STOPWORDS
from fake_useragent import UserAgent

#__all__ = ['googleWordCloudFn']

def getWebPage(url):  
    
    import requests
    
    ua = UserAgent()
    headers = {'User-Agent': str(ua.chrome)}
    url = url.replace(' ','+')   
    
    try:
        page = requests.get(url,headers=headers)
        
        # raise an error if the page is not read in properly
        if page.status_code != 200:
            page.raise_for_status()
        else:
            # random delay to reduce the chance of spamming server
            delay_time = 5; #np.random.randint(1,60)
            print("Delay time: " + str(delay_time))
            time.sleep(delay_time) 
            
            
    except requests.exceptions.HTTPError:
        print("Webpage could not be read")
        print(page)
        sys.exit()
              
    return page


def getAbstractsFromGooglePage(page):
    
    try:
        soup = BeautifulSoup(page.content, 'html.parser')
    except:
        soup = BeautifulSoup(page.content)
        
        
    searchResults = soup.find_all('div',{'class':'srg'})
    
    abstractText = ""
    for searchResult in searchResults:
    
        try:
            newTexts = searchResult.find_all('span',{'class':'st'})
            for newText in newTexts:
                try:                
                    abstractText = abstractText+" "+newText.text
                except:
                    print("New text not found")
        except:
            print("No new search results found")


    return abstractText


def createWordCloud(text,searchTerm):
    """
    Create the word cloud based on the provided text and save to searchTerm.png

    Parameters
    ----------
    text : STRING
        A long string of text/words
    searchTerm : STRING
        The created word cloud will be saved to searchTerm.png.

    Returns
    -------
    None. - saves "searchTerm.png" word cloud

    """
    stopwords = set(STOPWORDS)
        
    wc = WordCloud(background_color="white", 
                   max_words=200, 
                   stopwords=stopwords, 
                   mask=None, 
                   collocations=True, 
                   width=1000, height=800)
    
    # generate word cloud
    wc.generate(text)
    
    # show
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(searchTerm + '.png')
    
    

def createGoogleWordCloud(searchTerm):
    """
    This function creates a word cloud from the defined searchTerm and saves
    a png to the current directory

    Parameters
    ----------
    searchTerm : STRING
        The search term you wish to google.

    Returns
    -------
    None. - saves "searchTerm.png" word cloud based on the google results

    """
    
    url = "https://www.google.co.uk/search?q="+searchTerm
    
    page = getWebPage(url)
    
    text = getAbstractsFromGooglePage(page)    
    
    createWordCloud(text,searchTerm)

