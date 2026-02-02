
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

if __name__ == '__main__':
    # 测试数据库连接
    client = get_mongodb_client()
    if client:
        print("✅ MongoDB连接测试成功")
        client.close()
    else:
        print("⚠️  无法连接到MongoDB，表单数据将无法保存")
    
    app.run(debug=True, host='0.0.0.0', port=5000)