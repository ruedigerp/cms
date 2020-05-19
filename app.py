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
    return render_template("index.html", dict_item = master_dictionary)

def p_debug(str):
    app.logger.info("Debug: ", str)
    return

@app.route('/editor/meta/save', methods=['POST'])
def savemetadata():
    type   = request.form.get('type')
    id     = request.form.get('id')
    author = request.form.get('author')
    title = request.form.get('title')
    meta_data = {"id": id, "type": type, "data": { "title": title, "author": author } }
    write_meta(id,meta_data);
    return redirect("/editor/list")

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
    # print (content)
    return json.dumps(content)

@app.route("/editor/<str>", methods=["GET"])
def editor(str):
    data = open('data/'+str+'.json','r').read()
    return render_template("editor.html", data=data, id=str )

@app.route("/view/<id>", methods=["GET"])
def view(id):
    read_data(id)
    return render_template("view.html", id=id )


@app.route("/editor/new", methods=["GET"])
def newarticle():
    dateTimeObj = datetime.now()
    id = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S-%f")
    write_data(id,"")
    write_new_meta(id)
    return redirect("/editor/"+id);

@app.route("/editor/meta/edit/<id>", methods=["GET"])
def meta_edit(id):
    dict_item = read_meta_edit(id)
    return render_template("meta.html", dict_item=dict_item )

def to_pretty_json(value):
    return json.dumps(value, sort_keys=false,
                      indent=4, separators=(',', ': '))

def write_new_meta(id):
    meta_data = {}
    meta_data = {"id": id, "type": "draft", "data": { "title": "Neuer Article", "author": "Authorname" } }
    write_meta(id,meta_data);

def read_meta_edit(id):
    return json.loads(open('meta/' + id + '.json','r').read())

def read_meta():
    return json.loads(open('meta/articles.json','r').read())

def write_meta(id,data):
    with open("meta/" + id + ".json", "w") as twitter_data_file:
        json.dump(data, twitter_data_file, indent=4, sort_keys=True)

def read_data(id):
    return json.loads(open('data/' + id + '.json','r').read())

def write_data(id,data):
    print ("id: " + id)
    with open("data/"+id+".json", "w") as twitter_data_file:
        json.dump(data, twitter_data_file, indent=4, sort_keys=True)

def save_articles(articles, filepath):
    with open(filepath, "w") as f:
        json.dump(articles, f, indent=4)
    return None

app.jinja_env.filters['tojson_pretty'] = to_pretty_json

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0', port=4006)
