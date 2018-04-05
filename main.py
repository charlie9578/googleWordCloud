#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 21:47:00 2018

@author: charlie.plumley
"""

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time
import sys
from wordcloud import WordCloud, STOPWORDS



def getWebPage(url):
   
    from fake_useragent import UserAgent
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
    soup = BeautifulSoup(page.content, 'lxml')
              
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


def createWordCloud(text):
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
    plt.axis("off")
    
    return True


def googleWordCloud(searchTerm):
    url = "https://www.google.co.uk/search?q="+searchTerm
    
    page = getWebPage(url)
    
    text = getAbstractsFromGooglePage(page)    
    
    createWordCloud(text)

    return True


searchTerm = "resilience"

googleWordCloud(searchTerm)


