#!/usr/bin/env python
# coding: utf-8

# In[8]:


import gspread
import snscrape.modules.twitter as sntwitter
import pandas as pd


# In[9]:


gc = gspread.oauth()


# In[14]:


cities_list = ['Jaipur','Lucknow','Kolkata','Thane']

for city in cities_list:

    # Creating list to append tweet data to
    tweets_list1 = []

    q_str = "verified {0} (bed OR beds OR icu OR oxygen OR ventilator OR ventilators OR k) -'not verified' -'unverified' -'needed' -'need' -'needs' -'required' -'require' -'requires' -'requirement' -'requirements'"

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(q_str.format(city) + ' since:2020-04-25').get_items()):
        if i>100:
            break
        tweets_list1.append([tweet.date, tweet.content, tweet.username])

    # Creating a dataframe from the tweets list above 
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Text', 'Username'])
    tweets_df1['Datetime'] = tweets_df1['Datetime'].astype(str)
    tweets_df1['Datetime'] = tweets_df1['Datetime'].apply(lambda x : x[:19])
    tweets_df1 = tweets_df1[:50]
    print(city)
    sh = gc.open("Covid Tracker").worksheet(city)
    sh.resize(1)
    for i, row in tweets_df1.iterrows():
        sh.append_row(row.values.tolist())
    #     print(i)
        print(row)


# In[ ]:




