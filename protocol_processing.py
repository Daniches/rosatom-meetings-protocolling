from vosk import Model, KaldiRecognizer, SetLogLevel
from spacy.lang.ru import Russian
from spacy.matcher import PhraseMatcher
from nltk.stem.snowball import SnowballStemmer 
from docxtpl import DocxTemplate
from words2numbers.extractor import NumberExtractor
import sys
import os
import wave
import subprocess
import re
import datetime
import settings


SetLogLevel(0)
model = Model("model")
rec = KaldiRecognizer(model, settings.sample_rate)
numExtractor = NumberExtractor()

def process(file_name, file_name_out):
    
    result_merged = ''
    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                file_name,
                                '-ar', str(settings.sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                                stdout=subprocess.PIPE)
    while True:
        data = process.stdout.read(20000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = eval(rec.Result())
            result_merged = result_merged + ' ' + result['text']
    print(result_merged);
    result_merged = re.sub('[^a-zа-яё]', ' ', result_merged, flags=re.IGNORECASE)
    result_split = list(filter(None, result_merged.split(' ')))
    
    stemmer = SnowballStemmer("russian") 
    result_stem = [stemmer.stem(word) for word in result_split]
    result_stem_merged = ' '.join(result_stem)
    
    nlp = Russian()
    phrase_matcher = PhraseMatcher(nlp.vocab)
    
    key_phrases = []
    with open(settings.keywords_file) as file:
        lines = file.read().split('\n')
        for i in range(len(lines)):
            line = lines[i]
            key_phrases.append(line)
            phrase = ' '.join([stemmer.stem(word) for word in line.split(' ')])
            pattern = nlp(phrase)
            phrase_matcher.add("KEYPHRASE_"+str(i), [pattern]) 

    sentence = nlp(result_stem_merged)
    matched_phrases = phrase_matcher(sentence) 
    
    block_parts = []
    for match_id, start, end in matched_phrases:  
        string_id = nlp.vocab.strings[match_id]
        number_id = int(string_id.split('_')[-1])
        block_part = {
            'id' : number_id,
            'name' : key_phrases[number_id],
            'start' : start,
            'end': end
        }
        block_parts.append(block_part)
    
    for i in range(len(block_parts)):
        text_start = block_parts[i]['end']
        if i == len(block_parts)-1:
            text_end = len(result_split)
        else:
            text_end = block_parts[i+1]['start']
        block_parts[i]['text'] = ' '.join(result_split[text_start:text_end])
        block_parts[i]['text'] = numExtractor.replace_groups(block_parts[i]['text'])
    
    block_number = 1
    blocks = []
    block = []
    checked_key_phrases = [0 for i in key_phrases]
    
    for block_part in block_parts:
        if checked_key_phrases[block_part['id']] != 0:
            blocks.append(block)
            checked_key_phrases = [0 for i in key_phrases]
            block=[]
        block.append(block_part)
        checked_key_phrases[block_part['id']] = 1
    blocks.append(block)


    compiled_text = ''
    block_number = 1
    for block in blocks:
        compiled_text += f'{block_number}. '
        for block_part in block:
            compiled_text += f'{block_part["name"]}: {block_part["text"]}\n'
        compiled_text += '\n'
        block_number += 1
        
    
        
    doc = DocxTemplate(settings.template_file)
    context = { 'blocks' : compiled_text, 'date': f'{datetime.datetime.now():%d.%m.%Y}'}
    doc.render(context)
    doc.save(file_name_out)
