from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps
import os
from werkzeug.utils import secure_filename
import json

from helper import *


app = Flask(__name__)

UPLOAD_FOLDER = make_directory()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'thisisthesecretkey'

#decorator for login protected routes 
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        bearer = request.headers.get('Authorization')
        token = bearer.split(' ')[1]
        print(f"The token is --> {token}")

        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        
        try:
            data = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this'})


@app.route('/upload', methods=['POST'])
@token_required
def protected():
    error_message = ERROR_MESSAGE
    success_message = SUCCESS_MESSAGE

    handle = Handler(json.dumps(error_message), 400, 'application/json')
    
    if 'file' not in request.files:
        
        return handle.send_error_message()
       
    file = request.files['file'] 

    if file.filename == '':
        return handle.send_error_message()

    if file and allowed_file(file.filename):
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(success_message)
    return handle.send_error_message()    


@app.route('/login')
def login():
    
    
    if auth_user(request):
        username = request.args.get('client_id')
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'access_token': token, 'token_type': 'Bearer'})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)