from xml.dom.minidom import parse
from os import listdir
from collections import defaultdict, Counter
import os

from xml.dom.minidom import parse
import os
from os import listdir
from collections import defaultdict, Counter
def tokenize(sentence):
    return sentence.split()

def extract_context_words(sentence, entity_index, tokens):
    preceding_word = tokens[entity_index - 1] if entity_index > 0 else ""
    following_word = tokens[entity_index + 1] if entity_index < len(tokens) - 1 else ""
    return preceding_word, following_word


def extract_features(word):
    return {
        'length': len(word),
        'capitalization': 'all_caps' if word.isupper() else 'start_cap' if word[0].isupper() else 'lowercase',
        'suffix': word[-3:] if len(word) > 3 else word,
        'prefix': word[:3],
        'contains_number': any(char.isdigit() for char in word),
        'contains_special_char': any(not char.isalnum() for char in word),
        'word_count': len(word.split())
    }

def analyze_entity_word_structure(xml_path):
    doc = parse(xml_path)
    stats = defaultdict(lambda: {
        'lengths': [], 'capitalization': Counter(), 'suffixes': Counter(),
        'prefixes': Counter(), 'single_vs_multi_word': Counter(),
        'numbers': Counter(), 'special_chars': Counter(),
        'preceding_words': Counter(), 'following_words': Counter()
    })
    
    sentences = doc.getElementsByTagName("sentence")
    for sentence in sentences:
        sentence_text = sentence.getAttribute("text")
        entities = sentence.getElementsByTagName("entity")
        # Tokenisiere den Satztext
        tokens = tokenize(sentence_text)
        
        for entity in entities:
            entity_text = entity.getAttribute("text")
            entity_type = entity.getAttribute("type")
            
            features = extract_features(entity_text)
            
            # Finden Sie die Tokens, die der Entität entsprechen, und ihren Kontext
            # Dies ist eine vereinfachte Annäherung, die eine genauere Betrachtung benötigt
            entity_tokens = tokenize(entity_text)
            start_token = entity_tokens[0]
            end_token = entity_tokens[-1]
            
            # Versuchen Sie, den Start- und Endtoken der Entität im tokenisierten Satz zu finden
            start_index = tokens.index(start_token) if start_token in tokens else None
            end_index = tokens.index(end_token) if end_token in tokens else None
            
            # Erfassen Sie den Kontext basierend auf gefundenen Indizes
            preceding_word = tokens[start_index - 1] if start_index and start_index > 0 else ""
            following_word = tokens[end_index + 1] if end_index and end_index < len(tokens) - 1 else ""
            
            stats[entity_type]['preceding_words'][preceding_word] += 1
            stats[entity_type]['following_words'][following_word] += 1
            stats[entity_type]['lengths'].append(features['length'])
            stats[entity_type]['capitalization'][features['capitalization']] += 1
            stats[entity_type]['suffixes'][features['suffix']] += 1
            stats[entity_type]['prefixes'][features['prefix']] += 1
            stats[entity_type]['single_vs_multi_word'][features['word_count']] += 1
            stats[entity_type]['numbers'][features['contains_number']] += 1
            stats[entity_type]['special_chars'][features['contains_special_char']] += 1
    
    return stats

def analyze_entity_word_structure_in_folder(xml_folder):
    global_stats = defaultdict(lambda: {
        'lengths': [],
        'capitalization': Counter(),
        'suffixes': Counter(),
        'prefixes': Counter(),
        'single_vs_multi_word': Counter(),
        'numbers': Counter(),
        'special_chars': Counter(),
        'preceding_words': Counter(),
        'following_words': Counter()
    })

    for filename in listdir(xml_folder):
        if filename.endswith(".xml"):
            path = os.path.join(xml_folder, filename)
            document_stats = analyze_entity_word_structure(path)
            for entity_type, data in document_stats.items():
                for key, value in data.items():
                    if isinstance(value, Counter):
                        global_stats[entity_type][key].update(value)
                    else:
                        global_stats[entity_type][key].extend(value)

    return global_stats

def print_statistics(stats):
    for entity_type, data in stats.items():
        print(f"Entitätstyp: {entity_type}\n{'-' * 20}")
        print(f"Durchschnittliche Länge: {sum(data['lengths']) / len(data['lengths']) if data['lengths'] else 'N/A'}")
        print("Großschreibung:", dict(data['capitalization']))
        print("Häufigste Suffixe:", data['suffixes'].most_common(3))
        print("Häufigste Präfixe:", data['prefixes'].most_common(3))
        print("Einzelwort vs. Mehrwort:", dict(data['single_vs_multi_word']))
        print("Enthält Zahlen:", dict(data['numbers']))
        print("Enthält Sonderzeichen:", dict(data['special_chars']), "\n")
        print("Häufigste vorausgehende Wörter:", data['preceding_words'].most_common(3))
        print("Häufigste folgende Wörter:", data['following_words'].most_common(3))
        print("\n")

# Pfad zum Ordner mit XML-Dokumenten
xml_folder = "data/train/"
global_statistics = analyze_entity_word_structure_in_folder(xml_folder)

# Formatierter Ausdruck der Statistiken
print_statistics(global_statistics)
