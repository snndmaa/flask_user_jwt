# from user.models import User
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv
import pymongo
import jwt
import os


client = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = client.flask_test
load_dotenv()

# decorator for verifying the JWT
def token_required(f):
	
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		
		# jwt is passed in the request header
		try:
			if 'Bearer' in request.headers['Authorization']:
				token = request.headers['Authorization'].replace('Bearer ', '')
		except KeyError:
			return jsonify({ "error": "Authorization missing in Header!" })
		
		# return 401 if token is not passed
		if not token:
			return jsonify({'message' : 'Token is missing !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])

			current_user = db.users.find_one({ "_id": data['user_id'] })
		except:
			return jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
		# returns the current logged in user context to the routes
		
		return f(current_user, *args, **kwargs)

	return decorated