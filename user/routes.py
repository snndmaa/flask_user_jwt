from app import app
from user.models import User
from token_required import token_required


@app.route('/register', methods=['POST',])
@token_required
def signup():
    return User().signup()

@app.route('/login', methods=['POST',])
@token_required
def login():
    return User().login()