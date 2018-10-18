# Finnish-Dep-Parser-Wrapper

Wrapping up Finnish-dep-parser.

Annotates given text and outputs JSON.

## Getting Started

To execute, set environment variable
```
export FLASK_APP=src/run.py
```

Then run ``` flask run ```

### Prerequisites

Uses Python 3.5 or newer
Python libraries: flask, requests, nltk

## Usage

Can be used using POST or GET.

For GET
```
http://127.0.0.1:5000/?text=Helsingin%20kirjamessut%20perui%20Kiuas-kirjakustantamon%20osallistumisen%20messuille%20%E2%80%93%20Kustantamon%20taustalla%20%C3%A4%C3%A4rioikeistolaisista%20kommenteista%20tunnettu%20Timo%20H%C3%A4nnik%C3%A4inen
```
For POST
```
curl -d 'Helsingin kirjamessut perui Kiuas-kirjakustantamon osallistumisen messuille – Kustantamon taustalla äärioikeistolaisista kommenteista tunnettu Timo Hännikäinen' -H "Content-type: text/plain" -X POST http://127.0.0.1:5000/
```

### Configurations

The configurations for FiNER can be found in the ```src/config.ini```.

### Output

Example output:

```
{"0": [{"UPOS": "PROPN", "HEAD": 2, "XPOS": null, "DEPREL": "nmod:poss", "FEATS": {"Number": "Sing", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "", "PartForm": "", "Case": "Gen"}, "MISC": null, "DEPS": null, "LEMMA": "Helsinki", "FORM": "Helsingin"}, {"UPOS": "NOUN", "HEAD": 3, "XPOS": null, "DEPREL": "nsubj", "FEATS": {"Number": "Plur", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "", "PartForm": "", "Case": "Nom"}, "MISC": null, "DEPS": null, "LEMMA": "kirja#messut", "FORM": "kirjamessut"}, {"UPOS": "VERB", "HEAD": 0, "XPOS": null, "DEPREL": "root", "FEATS": {"Number": "Sing", "Mood": "Ind", "PronType": "", "AdpType": "", "NumType": "", "Tense": "Past", "Derivation": "", "VerbForm": "Fin", "Degree": "", "PartForm": "", "Case": ""}, "MISC": null, "DEPS": null, "LEMMA": "perua", "FORM": "perui"}, {"UPOS": "NOUN", "HEAD": 5, "XPOS": null, "DEPREL": "nmod:gsubj", "FEATS": {"Number": "Sing", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "", "PartForm": "", "Case": "Gen"}, "MISC": null, "DEPS": null, "LEMMA": "kiuas#kirja#kustantamo", "FORM": "Kiuas-kirjakustantamon"}, {"UPOS": "NOUN", "HEAD": 3, "XPOS": null, "DEPREL": "dobj", "FEATS": {"Number": "Sing", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "Minen", "VerbForm": "", "Degree": "", "PartForm": "", "Case": "Gen"}, "MISC": null, "DEPS": null, "LEMMA": "osallistua", "FORM": "osallistumisen"}, {"UPOS": "NOUN", "HEAD": 5, "XPOS": null, "DEPREL": "nmod", "FEATS": {"Number": "Plur", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "", "PartForm": "", "Case": "All"}, "MISC": null, "DEPS": null, "LEMMA": "messut", "FORM": "messuille"}, {"UPOS": "PUNCT", "HEAD": 3, "XPOS": null, "DEPREL": "punct", "FEATS": {"Number": "", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "", "PartForm": "", "Case": ""}, "MISC": null, "DEPS": null, "LEMMA": "–", "FORM": "–"}, {"UPOS": "NOUN", "HEAD": 9, "XPOS": null, "DEPREL": "nmod:poss", "FEATS": {"Number": "Sing", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "", "PartForm": "", "Case": "Gen"}, "MISC": null, "DEPS": null, "LEMMA": "kustantamo", "FORM": "Kustantamon"}, {"UPOS": "NOUN", "HEAD": 5, "XPOS": null, "DEPREL": "nmod", "FEATS": {"Number": "Sing", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "", "PartForm": "", "Case": "Ade"}, "MISC": null, "DEPS": null, "LEMMA": "tausta", "FORM": "taustalla"}, {"UPOS": "ADJ", "HEAD": 11, "XPOS": null, "DEPREL": "amod", "FEATS": {"Number": "Plur", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "Pos", "PartForm": "", "Case": "Ela"}, "MISC": null, "DEPS": null, "LEMMA": "ääri#oikeistolainen", "FORM": "äärioikeistolaisista"}, {"UPOS": "NOUN", "HEAD": 9, "XPOS": null, "DEPREL": "nmod", "FEATS": {"Number": "Plur", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "", "PartForm": "", "Case": "Ela"}, "MISC": null, "DEPS": null, "LEMMA": "kommentti", "FORM": "kommenteista"}, {"UPOS": "ADJ", "HEAD": 14, "XPOS": null, "DEPREL": "amod", "FEATS": {"Number": "Sing", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "Pos", "PartForm": "", "Case": "Nom"}, "MISC": null, "DEPS": null, "LEMMA": "tunnettu", "FORM": "tunnettu"}, {"UPOS": "PROPN", "HEAD": 14, "XPOS": null, "DEPREL": "name", "FEATS": {"Number": "Sing", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "", "PartForm": "", "Case": "Nom"}, "MISC": null, "DEPS": null, "LEMMA": "Timo", "FORM": "Timo"}, {"UPOS": "PROPN", "HEAD": 11, "XPOS": null, "DEPREL": "nmod", "FEATS": {"Number": "Sing", "Mood": "", "PronType": "", "AdpType": "", "NumType": "", "Tense": "", "Derivation": "", "VerbForm": "", "Degree": "", "PartForm": "", "Case": "Nom"}, "MISC": null, "DEPS": null, "LEMMA": "Hännikäinen", "FORM": "Hännikäinen"}]}%                                                                                                                                                                                  cs-111 finnish-dep-parser-wrapper 1310 % 

```

For each sentence, the api returns set of identified named entities. The sentences are index from 0 to n.
~                                                                                                          
