#coding:utf-8
import json
import random

with open("joke-dataset/reddit_jokes.json") as json_file:
    data_j_reddit = json.load(json_file)

def more_jokes():
    source=random.choice(["reddit"])
    #vide
    title="error"
    body="error"
    author="error"
    if source=="reddit":
        #reddit
        j=random.choice(data_j_reddit)
        title=j["title"]
        body=j["body"]
        author="reddit"
        
    
    return title,body,author


