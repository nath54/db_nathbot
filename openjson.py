#coding:utf-8
import json

with open("senator.json") as json_file:
    data = json.load(json_file)

print(data[0])




