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
## from urllib.parse import urljoin
# from flask_socketio import SocketIO, emit

# from urllib import urlopen

app = Flask(__name__)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/editor/list', methods = ["GET"])
def index():
    import os, fnmatch
    meta_data = read_meta()
    # print (meta_data)
    articles = meta_data['articles']
    articles = natsort.natsorted(articles,reverse=False)
    print ("articles: ", articles)
    files = []
    listOfFiles = os.listdir('data/')
    # listOfFiles.sort((key=lambda f: int(filter(str.isdigit, f)))
    listOfFiles = natsort.natsorted(listOfFiles,reverse=True)
    print("List: " + str(listOfFiles))
    pattern = "*.json"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            # print ("Entry: " + entry)
            x = entry.replace(".json", "")
            files.append(x)
    return render_template("index.html", len = len(files), listOfFiles = files, dict_item = articles)

@app.route('/postjson/<str>', methods = ['POST'])
def postJsonHandler(str):
    print (request.is_json)
    content = request.get_json()
    print (content)
    write_data(str,content)
    return 'JSON posted'

@app.route('/getjson/<id>', methods = ['GET'])
def getJsonHandler(id):
    content = read_data(id)
    print (content)
    return json.dumps(content)

@app.route("/editor/<str>", methods=["GET"])
def editor(str):
    data = open('data/'+str+'.json','r').read()
    return render_template("editor.html", data=data, id=str )

@app.route("/view/<id>", methods=["GET"])
def view(id):
    # data = open('data/'+id+'.json','r').read()
    read_data(id)
    return render_template("view.html", id=id )


@app.route("/editor/new", methods=["GET"])
def newarticle():
    dateTimeObj = datetime.now()
    id = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S-%f")
    print ("ID: " + id)
    write_data(id,"")
    write_new_meta(id)
    return redirect("/editor/"+id);

def to_pretty_json(value):
    return json.dumps(value, sort_keys=false,
                      indent=4, separators=(',', ': '))

def write_new_meta(id):
    meta_data = read_meta()
    print ("Meta: ", meta_data)
    meta_data['articles'].append({"id": id, "type": "draft", "data": { "title": "Neuer Article", "author": "Authorname" } })
    # meta_data.articles.blocks['id'] = id
    print ("Meta_data: ", meta_data)
    write_meta(meta_data);

def read_meta():
    # data = json.loads(open('data/data.json','r').read())
    return json.loads(open('meta/articles.json','r').read())

def write_meta(data):
    # print ("id: " + id)
    with open("meta/articles.json", "w") as twitter_data_file:
        json.dump(data, twitter_data_file, indent=4, sort_keys=True)

def read_data(id):
    # data = json.loads(open('data/data.json','r').read())
    return json.loads(open('data/'+id+'.json','r').read())

def write_data(id,data):
    print ("id: " + id)
    with open("data/"+id+".json", "w") as twitter_data_file:
        json.dump(data, twitter_data_file, indent=4, sort_keys=True)

def save_articles(articles, filepath):
    """
        saves articles to a json file
        :param article a list of dict
        :param path of file to save
    """
    with open(filepath, "w") as f:
        json.dump(articles, f, indent=4)
    return None

app.jinja_env.filters['tojson_pretty'] = to_pretty_json

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0', port=4006)
