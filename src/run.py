from flask import Flask
from flask import request
import argparse
import sys, os
from run_finnish_dep_parser import RunFinDepParser
import logging, json
import re
import time
import datetime
import nltk
import nltk.data
import xml.dom.minidom

app = Flask(__name__)


@app.before_request
def before_request():
    if True:
        print("HEADERS", request.headers)
        print("REQ_path", request.path)
        print("ARGS",request.args)
        print("DATA",request.data)
        print("FORM",request.form)

def parse_input(request):
    input = None
    if request.method == 'GET':
        text = request.args.get('text')
        sentences = tokenization(text)
        input = {i: sentences[i] for i in range(0, len(sentences))}
    else:
        if request.headers['Content-Type'] == 'text/plain':
            sentences = tokenization(str(request.data.decode('utf-8')))
            input = {i:sentences[i] for i in range(0, len(sentences))}
            print("data", input)
        else:
            print("Bad type", request.headers['Content-Type'])
    return input

def tokenization(text):
    print('Tokenize this', text)
    tokenizer = nltk.data.load('tokenizers/punkt/finnish.pickle')
    return tokenizer.tokenize(text)


@app.route('/', methods=['POST', 'GET'])
def index():
    input_data = parse_input(request)
    if input_data != None:
        depParser = RunFinDepParser(input_data)
        depParser.run()
        code = depParser.parse()

        if code == 1:
            results = depParser.get_json_string()
            print('results',results)
            return str(results)
            #return "Success"
        else:
            return results.toprettyxml()
    return "415 Unsupported Media Type ;)"