from flask import render_template, request, session, redirect, url_for
from flask_jsonpify import jsonify
from flask import Flask, flash, redirect, render_template, request, session, abort, current_app
from flask_restful import Resource, Api
from flask_cors import CORS
import sys
import re
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
# import json
# import os,fnmatch
# import logging
# import requests
# import time
# import natsort
# from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/status', methods=["GET"])
def apistatus():
    return jsonify({"status":"ok"})

# Rewrite / to /admin/
@app.route('/', methods = ["GET"] )
def redirectTo():
    return redirect('/admin/')

# App Route Adminpanel
@app.route('/admin/', methods = ["GET"] )
def contentList():
    return render_template("index.html")

# App Route Editor
#
# Todo: autosave="1" in env or config
#
@app.route('/admin/editor.html/<id>', methods = ["GET"] )
def contentEditor(id):
    return render_template("editor.html", id=id, autosave="1")

@app.route('/admin/pages.html', methods = ["GET"] )
def pagesList():
    return render_template("pages.html")

@app.route('/admin/page.html/<id>', methods = ["GET"] )
def pageEditor(id):
    return render_template("page.html", id=id)

@app.route('/admin/menu.html', methods = ["GET"] )
def menuEditor():
    return render_template("menu.html", id="1")

@app.route('/admin/meta.html/<id>', methods = ["GET"] )
def metaEditor(id):
    return render_template("meta.html", id=id)

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0', port=8081)
