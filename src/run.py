from flask import Flask, jsonify
from flask import request, abort
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
import csv, traceback

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
    env = 'DEFAULT'
    if request.method == 'GET':
        text = request.args.get('text')
        input = {0:text}
    else:
        if request.headers['Content-Type'] == 'text/plain':
            text = str(request.data.decode('utf-8'))
            input = {0: text}
        else:
            print("Bad type", request.headers['Content-Type'])
    print('---------------------------------------------------')

    # read environment from environment variable
    try:
        env = os.environ['FDP_CONFIG_ENV']
    except KeyError as kerr:
        print("Environment variable FDP_CONFIG_ENV not set:", sys.exc_info()[0])
        traceback.print_exc()
        env = None
        abort(500, 'Problem with setup: internal server error')
    except Exception as err:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc()
        env = None
        abort(500, 'Unexpected Internal Server Error')

    return input, env

def tokenization(text):
    print('Tokenize this', text)
    tokenizer = setup_tokenizer()
    return tokenizer.tokenize(text)

def setup_tokenizer():
    tokenizer = nltk.data.load('tokenizers/punkt/finnish.pickle')
    with open('language-resources/abbreviations.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            print("Add abbreviation", row[0])
            tokenizer._params.abbrev_types.add(row[0])
    return tokenizer

@app.route('/', methods=['POST', 'GET', 'OPTIONS'])
def index():
    input_data, env = parse_input(request)
    if input_data != None:
        depParser = RunFinDepParser(input_data, env)
        depParser.run()
        code = depParser.parse()
        results = depParser.get_json()

        if code == 1:
            #print('results',results)
            data = {'status': 200, 'data': results, 'service':"Finnish-dep-parser wrapper", 'date':dt.today().strftime('%Y-%m-%d')}
            return jsonify(data)
        else:
            data = {'status': -1, 'error': results.toprettyxml(), 'service':"Finnish-dep-parser wrapper", 'date':dt.today().strftime('%Y-%m-%d')}
            return jsonify(json.dumps(data, ensure_ascii=False))
    
    data = {'status': -1, 'error': "415 Unsupported Media Type ;)", 'service':"Finnish-dep-parser wrapper", 'date':dt.today().strftime('%Y-%m-%d')}
    return jsonify(data)

