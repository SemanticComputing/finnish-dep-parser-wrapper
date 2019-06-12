from flask import Flask, jsonify
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
from datetime import datetime as dt

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
    print('----------------------PARSE DATA----------------------')
    input = None
    env = None
    if request.method == 'GET':
        text = request.args.get('text')
        sentences = tokenization(text)
        input = {i: sentences[i] for i in range(0, len(sentences))}

        opt_param = request.args.get("test")
        print('OPT PARAM', opt_param)
        if opt_param != None:
            env = "TEST"
        print('VALUE', env)
    else:
        if request.headers['Content-Type'] == 'text/plain':
            sentences = tokenization(str(request.data.decode('utf-8')))
            input = {i:sentences[i] for i in range(0, len(sentences))}
            print("data", input)

            opt_param = request.args.get("test")
            print('OPT PARAM', opt_param)
            if opt_param != None:
                env = "TEST"
            print('VALUE', env)
        else:
            print("Bad type", request.headers['Content-Type'])
    print('---------------------------------------------------')
    return input, env

def tokenization(text):
    print('Tokenize this', text)
    tokenizer = nltk.data.load('tokenizers/punkt/finnish.pickle')
    return tokenizer.tokenize(text)


@app.route('/', methods=['POST', 'GET'])
def index():
    input_data, env = parse_input(request)
    if input_data != None:
        depParser = RunFinDepParser(input_data, env)
        depParser.run()
        code = depParser.parse()
        results = depParser.get_json()

        if code == 1:
            print('results',results)
            data = {'status': 200, 'data': results, 'service':"Finnish-dep-parser wrapper", 'date':dt.today().strftime('%Y-%m-%d')}
            return jsonify(data)
            #return "Success"
        else:
            data = {'status': -1, 'error': results.toprettyxml(), 'service':"Finnish-dep-parser wrapper", 'date':dt.today().strftime('%Y-%m-%d')}
            return jsonify(json.dumps(data, ensure_ascii=False))
    
    data = {'status': -1, 'error': "415 Unsupported Media Type ;)", 'service':"Finnish-dep-parser wrapper", 'date':dt.today().strftime('%Y-%m-%d')}
    return jsonify(data)

