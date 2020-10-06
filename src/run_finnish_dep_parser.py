import configparser
import fnmatch
import json
import logging
import logging.config
import multiprocessing
import ntpath
import os
import os.path
import subprocess
from configparser import (DuplicateOptionError, DuplicateSectionError, Error,
                          MissingSectionHeaderError, NoOptionError,
                          NoSectionError, ParsingError)
from itertools import zip_longest
from multiprocessing import Process
from pathlib import Path
import traceback, sys

import requests
from flask import abort

from conllu import parse, parse_tree
from word import Word

logging.config.fileConfig(fname='conf/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger('depparser')

class RunFinDepParser:
    def __init__(self, input_texts, env):
        self.input_texts = list()
        if len(input_texts)>0:
            self.input_texts = input_texts

        self.folder = ""
        if not (self.folder.endswith("/")):
            self.folder += "/"

        self.file_extension = ""
        self.output_files = list()
        self.output_texts =dict()
        self.sentences_json = dict()
        self.sentences_data = dict()
        self.paragraph_data = dict()
        self.tool = ""
        self.pool_number = 4
        self.pool_size = 4

        self.read_configs(env)

    def read_configs(self, env):

        try:
            config = configparser.ConfigParser()
            config.read('conf/config.ini')

            if env in config:
                self.tool = config[env]['finnish_dep_parser_url']
                self.pool_number = int(config[env]['pool_number'])
                self.pool_size = int(config[env]['chunking'])
            elif env == None or len(env) == 0:
                err_msg = 'The environment is not set: %s' % (env)
                raise Exception(err_msg)
            else:
                if 'DEFAULT' in config:
                    self.tool = config['DEFAULT']['finnish_dep_parser_url']
                    self.pool_size = int(config['DEFAULT']['chunking'])
                    self.pool_number = int(config[env]['pool_number'])
                else:
                    err_msg = 'Cannot find section headers: %s, %s' % (env, 'DEFAULT')
                    raise MissingSectionHeaderError(err_msg)
        except Error as e:
            logger.error(e)
            logger.error("[ERROR] ConfigParser error: %s", sys.exc_info()[0])
            logger.error(traceback.print_exc())
            abort(500)
        except Exception as err:
            logger.error(err)
            logger.error("[ERROR] Unexpected error: %s", sys.exc_info()[0])
            logger.error(traceback.print_exc())
            abort(500)

    def run(self):
        files = None

        items = list(self.input_texts.items())
        logger.info('url: %s', self.tool)
        logger.info('items before: %s', items)
        if len(items) > 1:
            pool = multiprocessing.Pool(self.pool_number)
            chunksize = self.pool_size
            chunks = [items[i:i + chunksize] for i in range(0, len(items), chunksize)]

            files = pool.map(self.execute_depparser_parallel, chunks)
            pool.close()
            pool.join()
        else:
            files = self.execute_depparser(items)

        if files != None:
            for i, j in files[0].items():
                if i in self.output_texts:
                    logger.info('This already in: %s, %s', i, j)
                self.output_texts[i] = j

    def execute_depparser_parallel(self, data):

        outputtexts = dict()

        for tpl in data:
            ind =tpl[0]
            input_text = tpl[1]

            if len(input_text.split())> 0:
                output_file = str(self.folder)+"output/"+str(ind)+".txt"

                my_file = Path(output_file)

                output = self.summon_dep_parser(input_text)  # +str(output_file)
                outputtexts[ind] = output

        return outputtexts

    def execute_depparser(self, input):
        for ind in self.input_texts.keys():
            input_text = self.input_texts[ind]
            if len(input_text.split())> 0:
                output_file = str(self.folder)+"output/"+str(ind)+".txt"
                self.output_files.append(output_file)
                output = self.summon_dep_parser(input_text)
                self.output_texts[ind] = output

    def summon_dep_parser(self, input_text):
        output = ""
        command = self.contruct_command(input_text)
        if self.tool.startswith('http') or  self.tool.startswith('https'):

            payload = {'text': str(input_text)}
            r = requests.get(self.tool, params=payload)
            output = str(r.text)
        else:
            try:
                logger.info(command)
                output = subprocess.check_output(command, shell=True, executable='/bin/bash').decode("utf-8")
            except subprocess.CalledProcessError as cpe:
                logger.warning("Error: %s", cpe.output)
        return output

    def contruct_command(self, input_text):
        if self.tool.startswith('http') or self.tool.startswith('https'):
            pass
        else:
            return self.tool+str(" <<< '")+str(input_text.replace("'","").replace("\\","")) +str("'")

    def write_output(self, output, file):
        f = open(file, 'w')
        f.write(output)
        f.close()

    def find_input_files(self):
        for file in os.listdir(self.folder):
            if fnmatch.fnmatch(file, self.file_extension):
                self.input_texts.append(self.folder + str(file))

    def get_output_files(self):
        return self.output_files

    def get_input_files(self):
        return self.input_texts

    def get_tool(self):
        return self.tool

    def set_tool(self, tool):
        self.tool = tool

    def set_input_files(self, input):
        self.input_texts = input

    def parse(self):
        logger.info("Start to parse")
        words = list()
        words_json = list()
        for ind in self.output_texts.keys():
            if not (self.output_texts[ind].startswith('<?xml version="1.0" encoding="utf-8"?>')):
                datalist = [d for d in self.output_texts[ind].replace('# newdoc','').split('# newpar') if len(d.strip())>0]
                for h in range(0, len(datalist)):
                    self.paragraph_data[h] = dict()
                    data = datalist[h]
                    logger.info("Parse this: %s", data)
                    # conllu parse
                    sentences = parse(data)#parse(data)
                    logger.debug("%s, %s, %s, %s",ind, "input",sentences, len(sentences))
                    if len(sentences) > 0:
                        # Parse sentences to words
                        for i in range(0, len(sentences)):
                            words_json = list()
                            sentence = sentences[i]
                            logger.info("check metadata: %s",sentence.metadata)
                            text = self.extract_text_from_metadata(sentence.metadata)
                            # Parse words to word-objects
                            for j in range(0, len(sentence)):
                                token = sentence[j]
                                logger.debug("TOKEN keys: %s", token.keys())
                                logger.debug("TOKEN word: %s",token["form"])
                                w = Word(token["form"], token["upostag"], token["xpostag"], token["feats"], "Edge", token["id"], token["lemma"], token["head"], token["deprel"], token["deps"], token["misc"])
                                w.set_feat(token["feats"])
                                words.insert(j, w)
                                words_json.insert(j, w.json())

                            # save words to a sentence, render to json
                            self.sentences_data[i] = words
                            words = list()
                            self.sentences_json[i] = words_json
                            logger.debug("%s, %s", i, self.sentences_data[i])
                            logger.debug("text: %s", text)

                            if len(text) == 0 or text == None:
                                logger.debug("Build text")
                                text=self.build_text(self.sentences_data[i])

                            if i not in self.paragraph_data[h]:
                                self.paragraph_data[h][i]={'words':words_json, 'text':text}
            else:
                return 0
        return 1

    def extract_text_from_metadata(self, metadata):
        if metadata != None:
            if 'text' in metadata:
                return metadata['text']
        return ""

    def build_text(self, words):
        text = ""
        for w in words:
            print(w)
            text += w.get_word() + " "
        return text

    def get_json(self):
        return self.paragraph_data

    def get_json_string(self):
        return json.dumps(self.sentences_json, ensure_ascii=False)