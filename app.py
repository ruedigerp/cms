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

@app.route('/api/v1/status', methods=["GET"])
def apistatus():
    return jsonify({"status":"ok"})

# GET full Article list
@app.route('/api/v1/articles', methods = ["GET"])
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
    return json.dumps(master_dictionary)

# GET Article by ID
@app.route('/api/v1/articles/<id>', methods = ['GET'])
def getJsonHandler(id):
    content = read_data(id)
    return json.dumps(content)

# PUT Update Artcile
@app.route('/api/v1/articles/<id>', methods = ['PUT'])
def postJsonHandler(id):
    print (request.is_json)
    content = request.get_json()
    print (content)
    write_data(id,content)
    return jsonify({"result":"ok"})

# POST New Article
@app.route("/api/v1/articles", methods=["POST"])
def newarticle():
    callback = request.form.get('callback')
    dateTimeObj = datetime.now()
    id = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S-%f")
    write_data(id,"")
    write_new_meta(id)
    return redirect("http://"+callback+"/admin/editor.html/"+id);

# GET Metadata by ID
@app.route("/api/v1/metadata/<id>", methods=["GET"])
def meta_edit(id):
    content = read_meta_edit(id)
    return json.dumps(content)

# PUT Update Metadata
@app.route('/api/v1/metadata', methods=['PUT'])
def savemetadata():
    print (request.is_json)
    content = request.get_json()
    metadata = {}
    for a_dict in content:
        if a_dict['name'] != 'callback':
            metadata[a_dict['name']] = a_dict['value']
        if a_dict['name'] == 'id':
            id = a_dict['value']
    print ("metadata: ", metadata, " ID: ", id, file=sys.stderr)
    write_meta(id,metadata)
    return jsonify({"result":"ok"})

# GET full Page list
@app.route('/api/v1/pages', methods = ["GET"])
def pages():
    import os, fnmatch
    master_dictionary = {}
    listOfMetaFiles = os.listdir('pages/')
    listOfMetaFiles = natsort.natsorted(listOfMetaFiles,reverse=True)
    listOfMetaFiles = sorted(listOfMetaFiles)
    pattern = "*.json"
    for metaentry in listOfMetaFiles:
        if fnmatch.fnmatch(metaentry, pattern):
            filename = metaentry.replace(".json", "")
            print ("Filename:", filename)
            master_dictionary[filename] = read_page_data(filename)
    app.logger.info("Debug: ", master_dictionary)
    return json.dumps(master_dictionary)

# POST New Page
@app.route("/api/v1/pages", methods=["POST"])
def newpages():
    callback = request.form.get('callback')
    dateTimeObj = datetime.now()
    id = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S-%f")
    # write_data(id,"")
    write_new_page(id)
    return jsonify({"result": id})
    # return redirect("http://"+callback+"/admin/pages.html/"+id);

# GET Page by ID
@app.route('/api/v1/pages/<id>', methods = ['GET'])
def getPageById(id):
    content = read_page(id)
    return json.dumps(content)

# PUT Update Page
@app.route('/api/v1/pages', methods=['PUT'])
def udpatePageData():
    content = request.get_json()
    print ("content: ", content, file=sys.stderr)
    metadata = {}
    childs = []
    for a_dict in content:
        name = a_dict['name']
        value = a_dict['value']
        if "childs" in name:
            print ("Name: ", name, " Value: ", value, file=sys.stderr)
            childs.append(value)
        else:
            print ("Name: ", name, " Value: ", value, file=sys.stderr)
            metadata[name] = value
        if name == 'id':
            id = value
    metadata['childs'] = childs
    print ("MetaData: ", metadata, file=sys.stderr)
    write_page_data(id,metadata)
    # return json.dumps(metadata)
    return jsonify({"result":"ok"})

# GET Page by Name
@app.route('/api/v1/rewrite/<path:u_path>')
def rewrite(u_path):
    name = u_path
    print ("name: ", name, file=sys.stderr)
    id = pageIdByName(name)
    return jsonify({"id": id})

def pageIdByName(name):
    master_dictionary = {}
    listOfMetaFiles = os.listdir('pages/')
    listOfMetaFiles = natsort.natsorted(listOfMetaFiles,reverse=True)
    listOfMetaFiles = sorted(listOfMetaFiles)
    pattern = "*.json"
    for metaentry in listOfMetaFiles:
        if fnmatch.fnmatch(metaentry, pattern):
            filename = metaentry.replace(".json", "")
            print ("Filename:", filename, file=sys.stderr)
            metaData = read_page_data(filename)
            print ("MetaData: ", json.dumps(metaData), file=sys.stderr)
            if name in metaData['url']:
                app.logger.info("Debug: ", name)
                return metaData['id']
    app.logger.info("Debug: ", master_dictionary)
    return name

def p_debug(str):
    app.logger.info("Debug: ", str)
    return

def to_pretty_json(value):
    return json.dumps(value, sort_keys=false,
                      indent=4, separators=(',', ': '))

def write_new_page(id):
    page_data = {}
    page_data = {"id": id, "type": "page", "title": id, "author": "Authorname" , "url": "/" + id, "childs": ()}
    write_page(id,page_data);

def write_page(id,data):
    with open("pages/" + id + ".json", "w") as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)

def read_page_data(id):
    return json.loads(open('pages/' + id + '.json','r').read())

def read_page(id):
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

app.jinja_env.filters['tojson_pretty'] = to_pretty_json

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0', port=4006)
