from flask import Flask, jsonify, request, make_response, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from functools import wraps
from settings import db
import re, random, string

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = db
short = PyMongo(app).db.short_data

def check_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None

class RouterMethods:
    @staticmethod
    def shorten():
        def get_valid_url():
            url = request.json['url']

            if check_url(url):
                return url
            elif check_url('https://' + url):
                return 'https://' + url
            else:
                return 'invalid url'

        url_code = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in
            range(7))

        if check_url(get_valid_url()):
            code_exists = short.find_one({'long_url': get_valid_url()})

            if(code_exists == None):
                created_id = short.insert_one({
                    "long_url": get_valid_url(),
                    "url_code": url_code,
                    "shortened_url": request.host_url + url_code
                })

                created_data = short.find_one({'_id': ObjectId(str(created_id.inserted_id))})

                return jsonify({"data": {
                    "long_url": created_data['long_url'],
                    "url_code": created_data['url_code'],
                    "shortened_url": created_data['shortened_url']
                }})
            else:
                return jsonify({"data": {
                    "long_url": code_exists['long_url'],
                    "url_code": code_exists['url_code'],
                    "shortened_url": code_exists['shortened_url']
                }})
        else:
            return jsonify({"data": {"error": "invalid url"}})
