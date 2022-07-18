from flask import Flask, render_template, request, redirect, url_for, jsonify
from token_required import token_required
import pymongo
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

# Databases
# client = pymongo.MongoClient(os.getenv('MONGO_URI'))
client = pymongo.MongoClient('mongodb+srv://sandman:sobriety@cluster0.lr58k.mongodb.net/?retryWrites=true&w=majority')
db = client.flask_test

# Routes
from user import routes
from template import routes

@app.get('/')
def home():
    return 'This is the homepage. Please use Postman to test the endpoints given in the Test File'


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)