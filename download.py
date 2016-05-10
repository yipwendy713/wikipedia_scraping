###Written by Wendy Yip wendyyip@gmail.com
###This code takes a category to be be searched in Wikipedia in the command line
###and downloads all the pages in Wikipeida associated with the category.  The articles
###are stored in a database called article.db with the category having its own table
###Each row in the table consists of an article topic associated with that category and the article text
###This program is written in python.  The table columns are "name" and "article_text"
###To run the program, type in the 
### command line  python download.py Cateogry1
### ex. python download.py Machine learning
### This program uses python's BeautifulSoup library, the Wikipedia API and Sqlite
#!/usr/bin/python
import sys
from bs4 import BeautifulSoup
import urllib
import re
import wikipedia
import sqlite3

#Function to retrieve article
def article_retrieve(url):
    #read in the url and call python's Beautiful Soup, web scrapping library

    wikihtml = urllib.urlopen(url)
    bsObj = BeautifulSoup(wikihtml,'lxml')
    topic=url.split('Category:')[1]
    topic=str(topic)
    
    article_link=[]
    
    #scrap names of articles with pages in the category specified by url

    for link in bsObj.find("div", {"id":"bodyContent"}).findAll("a",\
    href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            
            currentlink= link.attrs['href']
            currentlink=re.sub('/wiki/','',currentlink)
            currentlink=re.sub('_',' ',currentlink)
            currentlink=re.sub('%E2%80%93','-',currentlink)
            currentlink=re.sub('%E2%80%93','-',currentlink)
            article_link.append(currentlink)
            
    article_link=list(set(article_link))
    article_link.sort()
    
    # connect to article database
    # create a table for the current category with the column "name" for each article topic name
    # and "article_text" for the text of the Wikipedia article
    
    db = sqlite3.connect('article.db')
    cursor=db.cursor()
    cursor.execute('''CREATE TABLE '''+topic+''' (name TEXT PRIMARY KEY,\
                       article_text TEXT)''')
    #call wikipedia API to grab raw text of each article based on article title

    for i in range(0, len(article_link)):
        
        article_title=article_link[i]
        try:
            article_page=wikipedia.page(article_title)
            article_content=article_page.content
        
        except:
            None
        #store each article into table
        cursor.execute('''INSERT INTO ''' +topic+ '''(name, article_text)
                      VALUES(?,?)''', (article_title, article_content))
    
    db.commit()
    db.close()
   
    print'Wikipedia articles table called ' +topic+ ' has been created'
    return None

#read in subject to search in Wikipedia on commandline

#topic = sys.argv[-1]
topic = sys.argv[1:]
topic = ' '.join(topic)
print topic

#loop through all the categories in the input file

if topic=='':
    print 'There is no topic entered'
else: 
    try:      
        x=topic.split(' ')
        split_string=[i.lower() for i in x]
        topic=' '.join(split_string)
        topic=re.sub(' ','_',topic)
        url="https://en.wikipedia.org/wiki/Category:"+topic

        article_retrieve(url)
    except:
        
        print 'Search term is not a valid Wikipedia category'