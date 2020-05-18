from flask import render_template, request, session, redirect, url_for
from flask_jsonpify import jsonify
from flask import Flask, flash, redirect, render_template, request, session, abort, current_app
from flask_restful import Resource, Api
from flask_cors import CORS
# import pymysql
# from libs.UserSess import *
# from libs.SrvTree import *
import sys
import json
import os
import logging
import requests
import time
import re
import natsort
## import html
from datetime import datetime
## from flasgger import Swagger
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import os, fnmatch

def index():
    new_meta_data = {}
    new_meta_data['articles'] = []
    meta_data = read_meta()
    # print (meta_data)
    articles = meta_data['articles']
    articles = natsort.natsorted(articles,reverse=False)
    print "articles: ", articles, "\n"
    for item in articles:
        if ( item['id'] == "2020-05-17-02-23-47-145622" ):
            item['data']['title'] = "Testaenderung"
            print "Item: ", str(item), "\n"
        new_meta_data['articles'].append(item)
    print "articles: ", articles, "\n"
    # meta_data['articles'].append(item)
    print "meta: ", new_meta_data , "\n"
    write_meta(new_meta_data);
    # files = []
    # listOfFiles = os.listdir('data/')
    # listOfFiles = natsort.natsorted(listOfFiles,reverse=True)
    # print("List: " + str(listOfFiles))
    # pattern = "*.json"
    # for entry in listOfFiles:
    #     if fnmatch.fnmatch(entry, pattern):
    #         # print ("Entry: " + entry)
    #         x = entry.replace(".json", "")
    #         files.append(x)

def write_meta(data):
    # print ("id: " + id)
    with open("meta/articles.json", "w") as twitter_data_file:
        json.dump(data, twitter_data_file, indent=4, sort_keys=True)

def read_meta():
    # data = json.loads(open('data/data.json','r').read())
    return json.loads(open('meta/articles.json','r').read())

index()
