import os
import itertools
import re
import razdel

from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask_cors import CORS, cross_origin

import numpy as np
from sentence_transformers import SentenceTransformer
from scipy import spatial

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = "static"
RAW_FOLDER = "raw"
PROXY_FOLDER = "proxy"
SPLITTED_FOLDER = "splitted"
NGRAM_FOLDER = "ngramed"
DONE_FOLDER = "done"
RU_CODE = "ru"
ZH_CODE = "zh"

EMPTY_LINES = {"items": {"ru":[], "zh":[]}}
EMPTY_SIMS = {"items": {"ru":[], "zh":[], "sim":[]}}

pattern_ru_orig = re.compile(r'[a-zA-Z\(\)\[\]\/\<\>•\'\n]+')
double_spaces = re.compile(r'[\s]+')
double_commas = re.compile(r'[,]+')
double_dash = re.compile(r'[-—]+')
pattern_zh = re.compile(r'[」「“”„‟\x1a⓪①②③④⑤⑥⑦⑧⑨⑩⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽*a-zA-Zа-яА-Я\(\)\[\]\s\n\/\-\:•＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》【】〔〕〖〗〘〙〜〟〰〾〿–—‘’‛‧﹏〉]+')
pat_comma = re.compile(r'[\.]+')
first_numbers = re.compile(r'^[0-9,\.]+')
last_punct = re.compile(r'[,\.]+$')
multiple_spaces = re.compile(r'\s+')
pattern_ru = re.compile(r'[a-zA-Z\.\(\)\[\]\/\-\:!?\<\>;•\"\'«»——,]+')
pattern_ru_letters_only = re.compile(r'[^а-яА-Я\s]+')

model = SentenceTransformer('distiluse-base-multilingual-cased')

@app.route("/", methods=["GET", "POST"])
def index():
    return 0

@app.route("/items/<username>", methods=["GET", "POST"])
def items(username):
    create_folders(username)
    #load documents
    if request.method == "POST":
        if RU_CODE in request.files:
            file_ru = request.files["ru"]
            raw_ru = os.path.join(UPLOAD_FOLDER, username, RAW_FOLDER, RU_CODE, file_ru.filename)
            file_ru.save(raw_ru)
            split_to_sentences(file_ru.filename, RU_CODE, username)
        if ZH_CODE in request.files:
            file_zh = request.files["zh"]
            raw_zh = os.path.join(UPLOAD_FOLDER, username, RAW_FOLDER, ZH_CODE, file_zh.filename)
            file_zh.save(raw_zh)
            split_to_sentences(file_zh.filename, ZH_CODE, username)
        return {"res": 1}
    #return documents list
    files = {
        "items": {
            RU_CODE: get_files_list(username, RAW_FOLDER, RU_CODE),
            ZH_CODE: get_files_list(username, RAW_FOLDER, ZH_CODE)
        }
    }
    return files

def split_to_sentences(filename, langcode, username):
    raw = os.path.join(UPLOAD_FOLDER, username, RAW_FOLDER, langcode, filename)
    splitted = os.path.join(UPLOAD_FOLDER, username, SPLITTED_FOLDER, langcode, filename)
    with open(raw, mode='r', encoding='utf-8') as input_file, open(splitted, mode='w', encoding='utf-8') as out_file:
        if langcode == RU_CODE:
            lines = ' '.join(input_file.readlines())
            lines = re.sub(pattern_ru_orig, '', lines)
            lines = re.sub(double_spaces, ' ', lines)
            lines = re.sub(double_commas, ',', lines)
            lines = re.sub(double_dash, '—', lines)
            sentences = list(x.text for x in razdel.sentenize(lines))
        elif langcode == ZH_CODE:
            lines = ''.join(input_file.readlines())    
            lines = re.sub(pat_comma, '。', lines)
            sentences = list(re.sub(pattern_zh,'', x.strip()) for x in split_zh(lines))
        else:
            raise Exception("Unknown language code.")
        count = 1
        for x in sentences:
            if count < len(sentences)-1:
                out_file.write(x.strip() + "\n")
            else:
                out_file.write(x.strip())
            count += 1

def get_files_list(username, folder, lang):
    if not os.path.isdir(os.path.join(UPLOAD_FOLDER, username, folder, lang)):
        return []
    return os.listdir(os.path.join(UPLOAD_FOLDER, username, folder, lang))

def create_folders(username):
    if username and not os.path.isdir(os.path.join(UPLOAD_FOLDER, username)):
        os.mkdir(os.path.join(UPLOAD_FOLDER, username))
        create_subfolders(os.path.join(UPLOAD_FOLDER, username, RAW_FOLDER))
        create_subfolders(os.path.join(UPLOAD_FOLDER, username, SPLITTED_FOLDER))
        create_subfolders(os.path.join(UPLOAD_FOLDER, username, PROXY_FOLDER))
        create_subfolders(os.path.join(UPLOAD_FOLDER, username, NGRAM_FOLDER))
        create_subfolders(os.path.join(UPLOAD_FOLDER, username, DONE_FOLDER))

def create_subfolders(folder):
    os.mkdir(folder)
    os.mkdir(os.path.join(folder, RU_CODE))
    os.mkdir(os.path.join(folder, ZH_CODE))

def split_zh(paragraph):
    for sent in re.findall(u'[^!?。！？\.\!\?]+[!?。！？\.\!\?]?', paragraph, flags=re.U):
        yield sent

@app.route("/items/<username>/splitted/<lang>/<int:id>/<int:count>", methods=["GET"])
def splitted(username, lang, id, count):
    files = get_files_list(username, SPLITTED_FOLDER, lang)
    if len(files) < id+1:
        return EMPTY_LINES
    path = os.path.join(UPLOAD_FOLDER, username, SPLITTED_FOLDER, lang, files[id])    
    lines = []
    lines_count = 0
    symbols_count = 0
    if not os.path.isfile(path):
        return {"items":{lang:lines}}
    with open(path, mode='r', encoding='utf-8') as input_file:
        while True:
            line = input_file.readline()
            if not line:
                break
            lines_count+=1
            symbols_count+=len(line)
            if count>0 and lines_count>count:
                continue            
            lines.append(line)
    meta = {"lines_count": lines_count, "symbols_count": symbols_count}
    return {"items":{lang:lines}, "meta":{lang:meta}}

@app.route("/items/<username>/aligned/<lang>/<int:id>/<int:count>", methods=["GET"])
def aligned(username, lang, id, count):
    files = get_files_list(username, SPLITTED_FOLDER, lang)
    if len(files) < id+1:
        return EMPTY_LINES
    path = os.path.join(UPLOAD_FOLDER, username, DONE_FOLDER, lang, files[id])
    lines = []
    i = 0
    if not os.path.isfile(path):
        return {"items":{lang:lines}}
    with open(path, mode='r', encoding='utf-8') as input_file:
        while True:
            line = input_file.readline()
            if not line:
                break
            lines.append(line)
            i+=1
            if count>0 and i>=count:
                break
    return {"items":{lang:lines}}

@app.route("/items/<username>/align/<int:id_ru>/<int:id_zh>", methods=["GET"])
def align(username, id_ru, id_zh):
    batch_size = 50
    window = 20
    threshold = 0.5
    l_diff = 0.6
    batch_number = 0
    total_pairs = 0

    sentences_ru = []
    sentences_zh = []
    similarities = []

    files_ru = get_files_list(username, SPLITTED_FOLDER, RU_CODE)
    files_zh = get_files_list(username, SPLITTED_FOLDER, ZH_CODE)
    if len(files_ru) < id_ru+1 or len(files_zh) < id_zh+1:
        return EMPTY_SIMS

    splitted_ru = os.path.join(UPLOAD_FOLDER, username, SPLITTED_FOLDER, RU_CODE, files_ru[id_ru])
    splitted_zh = os.path.join(UPLOAD_FOLDER, username, SPLITTED_FOLDER, ZH_CODE, files_zh[id_zh])
    output_ru = os.path.join(UPLOAD_FOLDER, username, DONE_FOLDER, RU_CODE, files_ru[id_ru])
    output_zh = os.path.join(UPLOAD_FOLDER, username, DONE_FOLDER, ZH_CODE, files_zh[id_zh])

    with open(splitted_ru, mode="r", encoding="utf-8") as input_ru, \
         open(splitted_zh, mode="r", encoding="utf-8") as input_zh:
        #  ,open(ngramed_proxy_ru, mode="r", encoding="utf-8") as input_proxy:
        lines_ru = input_ru.readlines()
        lines_zh = input_zh.readlines()
        #lines_ru_proxy = input_proxy.readlines()

    with open(output_ru, mode='w', encoding='utf-8') as out_ru, open(output_zh, mode='w', encoding='utf-8') as out_zh:
        for lines_ru_batch, lines_ru_proxy_batch, lines_zh_batch in get_batch(lines_ru, lines_zh, lines_zh, batch_size):
            batch_number += 1
            print("batch:", batch_number)            
            vectors1 = get_line_vectors(lines_zh_batch)
            vectors2 = get_line_vectors(lines_ru_batch)
            sim_matrix = get_sim_matrix(vectors1, vectors2, window)  
            # count = 0
            # for i in range(sim_matrix.shape[0]):
            #     for j in range(sim_matrix.shape[1]):
            #         if sim_matrix[i,j] >= threshold:
            #             count += 1
            # total_pairs += count
            res_ru, res_zh, res_ru_proxy, sims = get_pairs(lines_ru_batch, lines_zh_batch, lines_ru_proxy_batch, sim_matrix, threshold)
            for x,y,z,s in zip(res_ru, res_zh, res_ru_proxy, sims):
                out_ru.write(x)
                out_zh.write(y)
                sentences_ru.append(x)
                sentences_ru.append(y)
                similarities.append(s)
        
    return {"items": {"ru": sentences_ru, "zh":sentences_zh, "sims": similarities}}

def get_batch(iter1, iter2, iter3, n):
    l1 = len(iter1)
    l3 = len(iter3)
    k = int(round(n * l3/l1))    
    kdx = 0 - k
    for ndx in range(0, l1, n):
        kdx += k
        yield iter1[ndx:min(ndx + n, l1)], iter2[kdx:min(kdx + k, l3)], iter3[kdx:min(kdx + k, l3)]

def get_line_vectors(lines):
    return model.encode(lines)

def get_pairs(ru_lines, zh_lines, ru_proxy_lines, sim_matrix, threshold):
    ru = []
    zh = []
    ru_proxy = []
    sims = []
    for i in range(sim_matrix.shape[0]):
        for j in range(sim_matrix.shape[1]):
            if sim_matrix[i,j] >= threshold:
                ru.append(ru_lines[j])
                zh.append(zh_lines[i])
                ru_proxy.append(ru_proxy_lines[i])
                sims.append(sim_matrix[i,j])
                
    return ru,zh,ru_proxy,sims

def get_sim_matrix(ru_vec, ru_vec2, window=10):
    sim_matrix = np.zeros((len(ru_vec), len(ru_vec2)))
    k = len(ru_vec)/len(ru_vec2)
    for i in range(len(ru_vec)):
        for j in range(len(ru_vec2)):
            if (j*k > i-window) & (j*k < i+window):
                sim = 1 - spatial.distance.cosine(ru_vec[i], ru_vec2[j])
            sim_matrix[i,j] = sim

    return sim_matrix 

if __name__ == "__main__":
    app.run(port=12000, debug=True)

