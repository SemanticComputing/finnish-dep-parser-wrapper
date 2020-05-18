import logging
import logging.config

from morphologicalfeatures import MorphologicalFeatures

logging.config.fileConfig(fname='conf/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger('doc')

class Word:
    def __init__(self, word, upos, uposx, feat, edge, id, lemma, head, deprel, deps, misc):
        self.lemma = lemma
        self.word = word
        self.upos = upos
        self.uposx = uposx
        self.edge = edge
        self.feat = MorphologicalFeatures()
        self.set_feat(feat)
        self.id = int(id)
        self.head = head
        self.deprel = deprel
        self.deps = deps
        self.misc = misc
        
    def get_word(self):
        return self.word

    def get_upos(self):
        return self.upos

    def get_feat(self):
        return self.feat

    def get_id(self):
        return self.id

    def set_feat(self, feat):
        self.feat.parse(feat)

    def get_edge(self):
        return self.edge

    def set_edge(self, edge):
        self.edge = edge

    def word_type_match(self, u, c, n):
        if self.upos == u:
            if self.feat.match(c, n) == True:
                return True
        return False

    def isFirstLetterUpperCase(self):
        letter = self.get_word()[:1]
        return letter.isupper()

    def json(self):
        data = {'ID':self.id,'FORM':self.word, 'LEMMA':self.lemma, 'UPOS':self.upos, 'XPOS':self.uposx, 'EDGE':self.edge, 'FEATS':self.feat.json(), 'HEAD':self.head, 'DEPREL':self.deprel, 'DEPS':self.deps, 'MISC':self.misc}
        return data

    def __repr__(self):
        return self.word

    def __str__(self):
        s = str(self.id) + ": " + self.word + ", " + self.upos
        return s

    def __hash__(self):
        return hash((self.word))

    def __eq__(self, other):
        if self.word != other.get_word():
            return False

        if self.id != other.get_id():
            return False

        if self.upos != other.upos():
            return False

        return True
