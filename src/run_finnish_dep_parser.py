import subprocess
import fnmatch
import os, json
import ntpath
import logging, requests
import os.path
from pathlib import Path
import configparser
from conllu import parse
from word import Word

logger = logging.getLogger('Finer')
hdlr = logging.FileHandler('finer.log')
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

class RunFinDepParser:
    def __init__(self, input_texts):
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


        self.read_configs()

    def read_configs(self):

        config = configparser.ConfigParser()
        config.read('src/config.ini')

        self.tool = config['DEFAULT']['finnish_dep_parser_url']

    def run(self):
        from itertools import zip_longest
        from multiprocessing import Process
        import multiprocessing
        pool = multiprocessing.Pool(4)

        files = None


        items = list(self.input_texts.items())
        if len(items) > 1:
            chunksize = 4
            chunks = [items[i:i + chunksize] for i in range(0, len(items), chunksize)]

            files = pool.map(self.execute_finer_parallel, chunks)
            pool.close()
            pool.join()
        else:
            files = self.execute_finer(items)

        if files != None:
            for f in files:
                self.output_files.extend(f)

    def execute_finer_parallel(self, data):

        tmp_output_files = list()

        for tpl in data:
            ind =tpl[0]
            input_text = tpl[1]

            if len(input_text.split())> 1:
                output_file = str(self.folder)+"output/"+str(ind)+".txt"
                #print("IN=",input_text)
                #print("OUT=", output_file)
                tmp_output_files.append(output_file)
                my_file = Path(output_file)
                if not(my_file.exists()):

                    output = self.summon_dep_parser(input_text)  # +str(output_file)
                    self.output_texts[ind] = output
                    #self.write_output(output, output_file)
                else:
                    logging.info("File %s exists, moving on", output_file);
        return tmp_output_files



    def execute_finer(self, input):
        for ind in self.input_texts.keys():
            input_text = self.input_texts[ind]
            if len(input_text.split())> 1:
                output_file = str(self.folder)+"output/"+str(ind)+".txt"
                self.output_files.append(output_file)
                output = self.summon_dep_parser(input_text)
                self.output_texts[ind] = output
                #self.write_output(output, output_file)

    def summon_dep_parser(self, input_text):
        output = ""
        command = self.contruct_command(input_text)
        if self.tool.startswith('http'):
            print(self.tool)
            payload = {'text': str(input_text)}
            r = requests.get(self.tool, params=payload)

            print(r.text)
            output = str(r.text)
        else:
            try:
                logging.info(command)
                output = subprocess.check_output(command, shell=True, executable='/bin/bash').decode("utf-8")
            except subprocess.CalledProcessError as cpe:
                logging.warning("Error: %s", cpe.output)
        return output

    def contruct_command(self, input_text):
        if self.tool.startswith('http'):
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
        words = list()
        words_json = list()
        for ind in self.output_texts.keys():
            data = self.output_texts[ind]
            if not(data.startswith('<?xml version="1.0" encoding="utf-8"?>')):
                sentences = parse(data)
                print("input",sentences)
                # Parse sentences to words
                for i in range(0, len(sentences)):
                    sentence = sentences[i]
                    # Parse words to word-objects
                    for j in range(0, len(sentence)):
                        token = sentence[j]
                        #print("TOKEN",token, i)
                        #print("TOKEN keys", token.keys())
                        print("TOKEN word",token["form"])
                        #return 1
                        w = Word(token["form"], token["upostag"], token["xpostag"], token["feats"], "EDGE", token["id"], token["lemma"], token["head"], token["deprel"], token["deps"], token["misc"])
                        w.set_feat(token["feats"])
                        words.insert(j, w)
                        words_json.insert(j, w.json())

                    # save words to a sentence, render to json
                    self.sentences_data[i] = words
                    words = list()
                    self.sentences_json[i] = words_json
            else:
                return 0
        return 1

    def get_json(self):
        return self.sentences_json

    def get_json_string(self):
        return json.dumps(self.sentences_json, ensure_ascii=False)


