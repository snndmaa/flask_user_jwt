from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from flask import Flask, jsonify, request
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
import jwt

class User:
    
    secret_key = os.environ.get('JWT_SECRET')

    def signup(self):
        
        #Create user object
        user = {
            '_id': uuid.uuid4().hex,
            'first_name': request.json.get('first_name'),
            'last_name': request.json.get('last_name'),
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }

        #Encrypt the password
        user['password'] = generate_password_hash(user['password'])

        #Check for an existing email address
        if db.users.find_one({ "email": user["email"] }):
            return jsonify({ "error": "Email is already in use!" }), 400

        #Non empty field validation
        if user['first_name'] and user['last_name'] and user['email'] and user['password']:
            db.users.insert_one(user)
            return jsonify(user), 201
        else:
            return jsonify({ "error": "Missing Fields(s)!" }), 400
    
    def login(self):

        auth = request.json

        #Non empty field validation
        if not auth or not auth.get('email') or not auth.get('password'):
            return jsonify({ "error": "Missing Field(s)!" })

        user = db.users.find_one({ "email": auth['email'] })

        if not user:
            return jsonify({ "error": "User does not Exist!" })

        #Check password and Create JWT
        if check_password_hash(user['password'], auth['password']):
            token = jwt.encode(
                { 'user_id': user['_id'], 'exp': datetime.utcnow() + timedelta(minutes=10) }, 
                self.secret_key, 
                algorithm="HS256"
            )
            
            return jsonify({ "token": token }), 201

        return jsonify({ "Error": "Incorrect User Credentials!" }), 403

