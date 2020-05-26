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
import os,fnmatch
import logging
import requests
import time
import re
import natsort
from dotenv import load_dotenv
# import os, fnmatch
## import html
from datetime import datetime
## from flasgger import Swagger
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
## from urllib.parse import urljoin
# from flask_socketio import SocketIO, emit
# from urllib import urlopen

app = Flask(__name__)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
cors = CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()
domain = os.environ.get("DOMAIN")

@app.route('/status', methods=["GET"])
def apistatus():
    return jsonify({"status":"ok"})

# Rewrite / to /home
@app.route('/', methods = ["GET"] )
def redirectToHome():
    url = domain + '/home'
    return redirect(url)

# GET Page by Name
@app.route('/<path:u_path>')
def catch_all(u_path):
    if u_path == "":
        upath = "home"
    children = ""
    content = ""
    data = []
    reqUrl = pageIdByName(u_path)
    id = reqUrl['id']
    page = read_page(id)
    pagetitle = page['title']
    pageauthor = page['author']
    pageid = id, " reqUrl: ", reqUrl
    menu = getMenu()
    for key in page['childs']:
        children = children + " " + key
        article = read_article(key)
        data.append(article)
    return render_template("viewpage.html", id=id, content=data, children=children, pagetitle=pagetitle,
        pageauthor=pageauthor, pageid=pageid, menu=menu["menu"] )

# GET Page by ID
@app.route('/page/<id>', methods = ['GET'])
def getPageById(id):
    children = ""
    content = ""
    data = []
    page = read_page(id)
    pagetitle = page['title']
    pageauthor = page['author']
    pageid = page['id']
    menu = getMenu()
    for key in page['childs']:
        children = children + " " + key
        article = read_article(key)
        data.append(article)
    return render_template("viewpage.html", id=id, content=data, children=children, pagetitle=pagetitle,
        pageauthor=pageauthor, pageid=pageid, menu=menu["menu"] )

####
# route for content direkt view
# @app.route('/content/<id>', methods = ['GET'])
# def getPageById(id):
#     ...
#     return Stuff
#
####

def getMenu():
    url = 'http://cms-api:4006/api/v1/menu/1'
    r = requests.get(url=url)
    return r.json()

def pageIdByName(name):
    url = 'http://cms-api:4006/api/v1/rewrite/' + name
    print ("url: ", url)
    r = requests.get(url=url)
    return r.json()

def read_page(id):
    url = 'http://cms-api:4006/api/v1/pages/' + id
    print ("url: " + url)
    r = requests.get(url=url)
    return r.json()

def read_article(id):
    url = 'http://cms-api:4006/api/v1/articles/' + id
    print ("url: " + url)
    r = requests.get(url=url)
    return r.json()

def to_pretty_json(value):
    return json.dumps(value, sort_keys=false,
                      indent=4, separators=(',', ': '))


##################################################
#
#  Old Stuff: test disable, if no errors, delete
#

# GET full Article list
@app.route('/api/v1/articles', methods = ["GET"])
def index():
    master_dictionary = {}
    listOfMetaFiles = os.listdir('meta/')
    listOfMetaFiles = natsort.natsorted(listOfMetaFiles,reverse=True)
    listOfMetaFiles = sorted(listOfMetaFiles)
    pattern = "*.json"
    for metaentry in listOfMetaFiles:
        if fnmatch.fnmatch(metaentry, pattern):
            filename = metaentry.replace(".json", "")
            print ("Filename:", filename)
            master_dictionary[filename] = read_meta_edit(filename)
    app.logger.info("Debug: ", master_dictionary)
    return json.dumps(master_dictionary)

def write_new_page(id):
    page_data = {}
    page_data = {"id": id, "type": "page", "title": id, "author": "Authorname" , "url": "/" + id, "childs": ()}
    write_page(id,page_data);

def write_page(id,data):
    with open("pages/" + id + ".json", "w") as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)

def read_page_data(id):
    return json.loads(open('pages/' + id + '.json','r').read())

def write_page_data(id,data):
    print ("id: " + id)
    with open("pages/"+id+".json", "w") as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)

def write_new_meta(id):
    meta_data = {}
    meta_data = {"id": id, "type": "draft", "title": id, "author": "Authorname" }
    write_meta(id,meta_data);

def read_meta_edit(id):
    return json.loads(open('meta/' + id + '.json','r').read())

def write_meta(id,data):
    with open("meta/" + id + ".json", "w") as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)

def read_data(id):
    return json.loads(open('data/' + id + '.json','r').read())

def write_data(id,data):
    print ("id: " + id)
    with open("data/"+id+".json", "w") as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)

def save_articles(articles, filepath):
    with open(filepath, "w") as f:
        json.dump(articles, f, indent=4)
    return None
#
# END Old Stuff
#
##################################################

app.jinja_env.filters['tojson_pretty'] = to_pretty_json

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0', port=8080)
