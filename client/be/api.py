import os
import itertools

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

@app.route("/", methods=["GET", "POST"])
def index():
    return 0

@app.route("/items/<username>", methods=["GET", "POST"])
def upload(username):
    create_folders(username)
    #load documents
    if request.method == "POST":
        if RU_CODE in request.files:
            file_ru = request.files["ru"]
            raw_ru = os.path.join(UPLOAD_FOLDER, username, RAW_FOLDER, RU_CODE, file_ru.filename)
            file_ru.save(raw_ru)
        if ZH_CODE in request.files:
            file_zh = request.files["zh"]
            raw_zh = os.path.join(UPLOAD_FOLDER, username, RAW_FOLDER, ZH_CODE, file_zh.filename)
            file_zh.save(raw_zh)
        return {"res": 1}
    #return documents list
    files = {
        "items": {
            RU_CODE: get_raw_files_list(username, RU_CODE),
            ZH_CODE: get_raw_files_list(username, ZH_CODE),
        }
    }
    return files

def get_raw_files_list(username, lang):
    return os.listdir(os.path.join(UPLOAD_FOLDER, username, RAW_FOLDER, lang))

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

@app.route("/split")
def split():
    return render_template("")

if __name__ == "__main__":
    app.run(port=12000, debug=True)