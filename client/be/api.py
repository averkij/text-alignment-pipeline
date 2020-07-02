import os
import itertools
import re
import razdel

from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask_cors import CORS, cross_origin

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
            ZH_CODE: get_files_list(username, RAW_FOLDER, ZH_CODE),
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
    i = 0
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

if __name__ == "__main__":
    app.run(port=12000, debug=True)

