from flask import Flask, jsonify, request, make_response, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from functools import wraps
from router import RouterMethods
from settings import db
import re

router = RouterMethods

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = db
short = PyMongo(app).db.short_data

@app.route('/', methods=['GET'])
def get_main_data():
    return "Main Route"

@app.route('/<code>', methods=['GET'])
def redir(code):
    data = short.find_one({"url_code": code})

    if data != None:
        return redirect(data['long_url'])
    else:
        return jsonify({"data": {
            "error": "invalid code"
        }})
        
@app.route('/shorten', methods=['GET'])
def get_shorten():
    return "Main Route"

@app.route('/shorten', methods=['POST'])
def shorten():
    return router.shorten()

if __name__ == '__main__':
    app.run(debug=True)

