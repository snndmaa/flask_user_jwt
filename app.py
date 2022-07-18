from flask import Flask, render_template, request, redirect, url_for, jsonify
from token_required import token_required
import pymongo
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

# Databases
client = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = client.flask_test

# Routes
from user import routes
from template import routes

@app.get('/')
def home():
    return 'Home'


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)