class MorphologicalFeatures:
    def __init__(self):
        self.case = ""
        self.number = ""
        self.mood = ""
        self.tense = ""
        self.person = ""
        self.voice = ""
        self.verbform = ""
        self.degree = ""
        self.partform = ""
        self.edge = ""
        self.adptype = ""
        self.numtype = ""
        self.derivation = ""
        self.prontype = ""

        self.unknown = True

    def get_case(self):
        return self.case

    def get_edge(self):
        return self.edge

    def set_case(self, case):
        self.case = case

    def get_number(self):
        return self.number

    def set_number(self, num):
        self.number = num

    def get_mood(self):
        return self.mood

    def get_tense(self):
        return self.tense

    def get_person(self):
        return self.person

    def get_verbform(self):
        return self.verbform

    def get_degree(self):
        return self.degree

    def get_partform(self):
        return self.partform

    def get_derivation(self):
        return self.derivation

    def get_prontype(self):
        return self.prontype

    def get_adptype(self):
        return self.adptype

    def get_numtype(self):
        return self.numtype

    def parse(self, feats):
        if feats == None:
            return
        print('features',feats)
        #print('features', feats.keys())
        if "Case" in feats:
            self.case = feats['Case']
        if "Number" in feats:
            self.number = feats['Number']
        if "Mood" in feats:
            self.mood = feats['Mood']
        if "Tense" in feats:
            self.tense = feats['Tense']
        if "Person" in feats:
            self.person = feats['Person']
        if "VerbForm" in feats:
            self.verbform = feats['VerbForm']
        if "Degree" in feats:
            self.degree = feats['Degree']
        if "PartForm" in feats:
            self.partform = feats['PartForm']
        if "Derivation" in feats:
            self.derivation = feats['Derivation']
        if "PronType" in feats:
            self.derivation = feats['PronType']
        if "AdpType" in feats:
            self.adptype = feats['AdpType']
        if "NumType" in feats:
            self.numtype = feats['NumType']
        if "Voice" in feats:
            self.voice = feats['Voice']

    def parse_str(self, feats):
        if "|" in feats:
            feat=feats.split("|")
            self.unknown = False

            for f in feat:
                if "Case" in f:
                    c = f.split("=")
                    self.case = c[1]
                if "Number" in f:
                    n = f.split("=")
                    self.number = n[1]
                if "Mood" in f:
                    n = f.split("=")
                    self.mood = n[1]
                if "Tense" in f:
                    n = f.split("=")
                    self.tense = n[1]
                if "Person=" in f:
                    n = f.split("=")
                    self.person = n[1]
                if "VerbForm" in f:
                    n = f.split("=")
                    self.verbform = n[1]
                if "Degree" in f:
                    n = f.split("=")
                    self.degree = n[1]
                if "PartForm" in f:
                    n = f.split("=")
                    self.partform = n[1]
                if "Derivation" in f:
                    n = f.split("=")
                    self.derivation = n[1]
                if "PronType" in f:
                    n = f.split("=")
                    self.prontype = n[1]

        elif "UNKNOWN" not in feats:
            self.unknown = False
            if "AdpType" in feats:
                n = feats.split("=")
                self.adptype = n[1]
            if "NumType" in feats:
                n = feats.split("=")
                self.numtype = n[1]
        else:
            self.unknown = True

    def match(self, c, n):
        if  self.case == c and self.number == n:
            return True
        else:
            return False

    def json(self):
        data = {"Case":self.case, "Number":self.number, "Tense":self.tense, "Mood":self.mood,"VerbForm":self.verbform, "Degree":self.degree, "PartForm":self.partform, "Derivation":self.derivation, "PronType":self.prontype, "AdpType":self.adptype, "NumType":self.numtype}
        return data

    def __str__(self):
        s = "Case="+str(self.case) + "|" + "Number="+str(self.number)
        return s

    def __eq__(self, other):
        if self.case != other.get_case():
            return False

        if self.number != other.get_number():
            return False

        if self.mood != other.get_mood():
            return False

        if self.tense != other.get_tense():
            return False

        if self.person != other.get_person():
            return False

        if self.verbform != other.get_verbform():
            return False

        if self.degree != other.get_degree():
            return False

        if self.partform != other.get_partform():
            return False

        if self.prontype != other.get_prontype():
            return False

        if self.derivation != other.get_derivation():
            return False

        if self.adptype != other.get_adptype():
            return False

        if self.numtype != other.get_numtype():
            return False

        return True