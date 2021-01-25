import argparse
import csv
import datetime
import json
import logging
import logging.config
import os
import re
import sys
import time
import traceback
import xml.dom.minidom
from datetime import datetime as dt
import cgi

import nltk
import nltk.data
from flask import Flask, abort, jsonify, request

from run_finnish_dep_parser import RunFinDepParser

logging.config.fileConfig(fname='conf/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger('run')

app = Flask(__name__)

@app.before_request
def before_request():
    if True:
        logger.info("HEADERS: %s", request.headers)
        logger.info("REQ_path: %s", request.path)
        logger.info("ARGS: %s",request.args)
        logger.info("DATA: %s",request.data)
        logger.info("FORM: %s",request.form)

def parse_input(request):
    logger.debug('----------------------PARSE DATA----------------------')
    input = None
    env = 'DEFAULT'
    if 'Content-Type' in request.headers:
        mimetype, options = cgi.parse_header(request.headers['Content-Type'])
        if request.method == 'GET':
            text = request.args.get('text')
            input = {0:text}
        else:
            if mimetype == 'text/plain':
                text = str(request.data.decode('utf-8'))
                input = {0: text}
            else:
                logger.warning("Bad type", mimetype)
        logger.debug('---------------------------------------------------')

        # read environment from environment variable
        try:
            env = os.environ['FDP_CONFIG_ENV']
        except KeyError as kerr:
            logger.error(kerr)
            logger.error("Environment variable FDP_CONFIG_ENV not set: %s", sys.exc_info()[0])
            logger.error(traceback.print_exc())
            env = None
            abort(500, 'Problem with setup: internal server error')
        except Exception as err:
            logger.error(err)
            logger.error("Unexpected error: %s", sys.exc_info()[0])
            logger.error(traceback.print_exc())
            env = None
            abort(500, 'Unexpected Internal Server Error')
    else:
        logger.error("Unable to process request, cannot retrieve content-type from the header %s" % (request.headers))

    return input, env

def tokenization(text):
    logger.debug('Tokenize this: %s', text)
    tokenizer = setup_tokenizer()
    return tokenizer.tokenize(text)

def setup_tokenizer():
    tokenizer = nltk.data.load('tokenizers/punkt/finnish.pickle')
    with open('language-resources/abbreviations.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            logger.debug("Add abbreviation: %s", row[0])
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
            logger.debug('results: %s',results)
            data = {'status': 200, 'data': results, 'service':"Finnish-dep-parser wrapper", 'date':dt.today().strftime('%Y-%m-%d')}
            return jsonify(data)
        else:
            data = {'status': -1, 'error': results.toprettyxml(), 'service':"Finnish-dep-parser wrapper", 'date':dt.today().strftime('%Y-%m-%d')}
            return jsonify(json.dumps(data, ensure_ascii=False))
    
    data = {'status': -1, 'error': "415 Unsupported Media Type ;)", 'service':"Finnish-dep-parser wrapper", 'date':dt.today().strftime('%Y-%m-%d')}
    return jsonify(data)
