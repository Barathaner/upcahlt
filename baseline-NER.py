#! /usr/bin/python3

import sys
from os import listdir,system
import re

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize

from util import evaluator

## dictionary containig information from external knowledge resources
## WARNING: You may need to adjust the path to the resource files
external = {}
with open("resources/HSDB.txt", encoding='utf-8') as h :
    for x in h.readlines() :
        external[x.strip().lower()] = "drug"
with open("resources/DrugBank.txt", encoding='utf-8') as h :
    for x in h.readlines() :
        (n,t) = x.strip().lower().split("|")
        external[n] = t

        
## --------- tokenize sentence ----------- 
## -- Tokenize sentence, returning tokens and span offsets

def tokenize(txt):
    offset = 0
    tks = []
    for t in word_tokenize(txt):
        offset = txt.find(t, offset)
        tks.append((t, offset, offset+len(t)-1))
        offset += len(t)
    return tks

## -----------------------------------------------
## -- check if a token is a drug part, and of which type



suffixes_drug = ['hloride', 'osphate', 'sodium', 'hydrate', 'pollen', 'acetate', 'sulfate']
suffixes_brand = ['relief', 'nitizer', 'trength', 'nscreen', 'eatment', 'odorant', 'tablets']



def classify_token(txt):

   # WARNING: This function must be extended with 
   #          more and better rules



   if txt.lower() in external : return external[txt.lower()]

   #txt = txt.lower()
   #elif txt[-7:] in suffixes_drug : return "drug"
   #elif txt[-7:] in suffixes_brand : return "brand"

   # achieves 45.7% F1

   elif (txt[0].isupper() and not txt.isupper() and len(txt) > 13): return "group"
   elif any(char.isdigit() for char in txt) and len(txt) > 8: return "drug_n"


   #elif txt[-3:] in ['ine'] : return "drug"

   #elif txt[-3:] in ['CIN'] : return "brand"
   
   
   
   # other rules, not very successful

   #elif any(txt.startswith(prefix) for prefix in prefixes_drug_n): return "drug_n"
   #elif any(txt.startswith(prefix) for prefix in prefixes_drug): return "drug"
   #elif any(txt.startswith(prefix) for prefix in prefixes_group): return "group"
   #elif any(txt.startswith(prefix) for prefix in prefixes_brand): return "brand"
   
   #if any(not char.isalnum() for char in txt) and len(txt) > 16: return "group"

   #elif len(txt) < 13 and txt.islower() : return "drug"

   #elif len(txt) >= 13 and txt.islower() : return "group"
   
   #if any(not char.isalnum() for char in txt) and len(txt) > 16: return "group"

   #elif txt.isupper() and len(txt) < 2: return "brand"

   #elif '-' in txt : return "drug"

   else : return "NONE"

   

## --------- Entity extractor ----------- 
## -- Extract drug entities from given text and return them as
## -- a list of dictionaries with keys "offset", "text", and "type"

def extract_entities(stext) :

    # WARNING: This function must be extended to
    #          deal with multi-token entities.
    
    # tokenize text
    tokens = tokenize(stext)
         
    result = []
    i = 0
    while i < len(tokens):
        token_txt, token_start, token_end = tokens[i]
        drug_type = classify_token(token_txt)

        # Check for multi-token entities
        if drug_type != "NONE":
            # Initialize multi-token entity variables
            entity_start = token_start
            entity_end = token_end
            entity_type = drug_type

            # Look ahead to see if the next token(s) are part of a multi-token entity
            j = i + 1
            while j < len(tokens):
                next_token_txt, next_token_start, next_token_end = tokens[j]
                next_drug_type = classify_token(next_token_txt)

                # Check if the next token is part of the current entity
                if next_drug_type == drug_type or (next_drug_type != "NONE" and entity_type in ["drug", "group"]):
                    entity_end = next_token_end
                    i = j
                else:
                    break
                j += 1

            # Add the entity to the results
            e = {
                "offset": str(entity_start) + "-" + str(entity_end),
                "text": stext[entity_start:entity_end + 1],
                "type": entity_type
            }
            result.append(e)
        i += 1

    return result
      
## --------- main function ----------- 

def nerc(datadir, outfile) :
   
    # open file to write results
    outf = open(outfile, 'w')

    # process each file in input directory
    for f in listdir(datadir) :
      
        # parse XML file, obtaining a DOM tree
        tree = parse(datadir+"/"+f)
      
        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences :
            sid = s.attributes["id"].value   # get sentence id
            stext = s.attributes["text"].value   # get sentence text
            
            # extract entities in text
            entities = extract_entities(stext)
         
            # print sentence entities in format requested for evaluation
            for e in entities :
                print(sid,
                      e["offset"],
                      e["text"],
                      e["type"],
                      sep = "|",
                      file=outf)
            
    outf.close()


   
## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir
## --

# directory with files to process
datadir = sys.argv[1]
outfile = sys.argv[2]

nerc(datadir,outfile)

evaluator.evaluate("NER", datadir, outfile)