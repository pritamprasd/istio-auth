from flask import Flask, jsonify, request
import requests
import os
from functools import wraps

app = Flask(__name__)

# API_URL="http://flask-app:80"
API_URL = os.environ.get("DOWNSTREAM_API")


def print_request_details(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Request Method: {request.method}")
        print(f"Request Path: {request.path}")
        print(f"Request Headers:{request.headers}")
        print(f"Request Parameters: {request.args}")
        print(f"Request Body: {request.data}")
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
@print_request_details
def index():
    return "Welcome to the Flask app!"

@app.route('/api/data1')
@print_request_details
def api_data1():
    data = {'message': 'This is sample API data 1'}
    return jsonify(data)

@app.route('/api/downstream')
@print_request_details
def api_data2():
    response = requests.get(f"{API_URL}/api/data1")
    if response.status_code == 200:
        data = {'message': response.json()}
    else:
        data = {
            'message': 'Downstream API Failed',
            'code': response.status_code,
            'error': response.text
        }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
