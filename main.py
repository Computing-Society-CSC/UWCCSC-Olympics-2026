
import flask
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import certifi
import urllib.parse

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')
