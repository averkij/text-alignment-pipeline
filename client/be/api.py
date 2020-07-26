import os
import pickle

from flask import Flask, request
from flask_cors import CORS
from mlflow import log_metric

import aligner
import constants as con
import helper
import splitter
from aligner import DocLine

app = Flask(__name__)

CORS(app)

EMPTY_LINES = {"items": {"ru":[], "zh":[]}}
EMPTY_SIMS = {"items": {"ru":[], "zh":[], "sim":[]}}

@app.route("/", methods=["GET", "POST"])
def index():
    return 0

@app.route("/items/<username>", methods=["GET", "POST"])
def items(username):
    helper.create_folders(username)
    #load documents
    if request.method == "POST":
        if con.RU_CODE in request.files:
            file_ru = request.files["ru"]
            raw_ru = os.path.join(con.UPLOAD_FOLDER, username, con.RAW_FOLDER, con.RU_CODE, file_ru.filename)
            file_ru.save(raw_ru)
            splitter.split_to_sentences(file_ru.filename, con.RU_CODE, username)
        if con.ZH_CODE in request.files:
            file_zh = request.files["zh"]
            raw_zh = os.path.join(con.UPLOAD_FOLDER, username, con.RAW_FOLDER, con.ZH_CODE, file_zh.filename)
            file_zh.save(raw_zh)
            splitter.split_to_sentences(file_zh.filename, con.ZH_CODE, username)
        return {"res": 1}
    #return documents list
    files = {
        "items": {
            con.RU_CODE: helper.get_files_list(username, con.RAW_FOLDER, con.RU_CODE),
            con.ZH_CODE: helper.get_files_list(username, con.RAW_FOLDER, con.ZH_CODE)
        }
    }
    return files

@app.route("/items/<username>/splitted/<lang>/<int:id>/<int:count>/<int:page>", methods=["GET"])
def splitted(username, lang, id, count, page):
    files = helper.get_files_list(username, con.SPLITTED_FOLDER, lang)
    if len(files) < id+1:
        return EMPTY_LINES
    path = os.path.join(con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang, files[id])    
    if not os.path.isfile(path):
        return {"items":{lang:[]}}

    lines = []
    lines_count = 0
    symbols_count = 0
    shift = (page-1)*count

    with open(path, mode='r', encoding='utf-8') as input_file:
        while True:
            line = input_file.readline()
            if not line:
                break
            lines_count+=1
            symbols_count+=len(line)
            if count>0 and (lines_count<=shift or lines_count>shift+count):
                continue
            lines.append((line, lines_count))

    total_pages = (lines_count//count) + (1 if lines_count%count != 0 else 0)
    meta = {"lines_count": lines_count, "symbols_count": symbols_count, "page": page, "total_pages": total_pages}
    return {"items":{lang:lines}, "meta":{lang:meta}}

@app.route("/items/<username>/aligned/<lang>/<int:id>/<int:count>", methods=["GET"])
def aligned(username, lang, id, count):
    files = helper.get_files_list(username, con.SPLITTED_FOLDER, lang)
    if len(files) < id+1:
        return EMPTY_LINES
    path = os.path.join(con.UPLOAD_FOLDER, username, con.DONE_FOLDER, lang, files[id])
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
    return {"items":{lang:lines[:5]}}

@app.route("/items/<username>/align/<int:id_ru>/<int:id_zh>", methods=["GET"])
def align(username, id_ru, id_zh):
    batch_size = 100
    window = 20
    threshold = 0.3
    l_diff = 0.6
    batch_number = 1
    total_pairs = 0

    sentences_ru = []
    sentences_zh = []
    similarities = []

    files_ru = helper.get_files_list(username, con.SPLITTED_FOLDER, con.RU_CODE)
    files_zh = helper.get_files_list(username, con.SPLITTED_FOLDER, con.ZH_CODE)
    if len(files_ru) < id_ru+1 or len(files_zh) < id_zh+1:
        return EMPTY_SIMS

    splitted_ru = os.path.join(con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, con.RU_CODE, files_ru[id_ru])
    splitted_zh = os.path.join(con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, con.ZH_CODE, files_zh[id_zh])
    output_ru = os.path.join(con.UPLOAD_FOLDER, username, con.DONE_FOLDER, con.RU_CODE, files_ru[id_ru])
    output_zh = os.path.join(con.UPLOAD_FOLDER, username, con.DONE_FOLDER, con.ZH_CODE, files_zh[id_zh])

    processing_ru = os.path.join(con.UPLOAD_FOLDER, username, con.PROCESSING_FOLDER, con.RU_CODE, files_ru[id_ru])

    with open(splitted_ru, mode="r", encoding="utf-8") as input_ru, \
         open(splitted_zh, mode="r", encoding="utf-8") as input_zh:
        #  ,open(ngramed_proxy_ru, mode="r", encoding="utf-8") as input_proxy:
        lines_ru = input_ru.readlines()
        lines_zh = input_zh.readlines()
        #lines_ru_proxy = input_proxy.readlines()

    docs = []
    with open(output_ru, mode='w', encoding='utf-8') as out_ru, open(output_zh, mode='w', encoding='utf-8') as out_zh:
        vectors1 = []
        vectors2 = []
        for lines_ru_batch, lines_ru_proxy_batch, lines_zh_batch in helper.get_batch(lines_ru, lines_zh, lines_zh, batch_size):
            print("batch:", batch_number)
            vectors1 += aligner.get_line_vectors(lines_zh_batch)
            vectors2 += aligner.get_line_vectors(lines_ru_batch)
            batch_number += 1

        sim_matrix = aligner.get_sim_matrix(vectors1, vectors2, window)
        res_ru, res_zh, res_ru_proxy, sims = aligner.get_pairs(lines_ru, lines_zh, lines_zh, sim_matrix, threshold)

        #write auto aligned lines
        for x,y,z,s in zip(res_ru, res_zh, res_ru_proxy, sims):
            out_ru.write(x)
            out_zh.write(y)
            sentences_ru.append(x)
            sentences_ru.append(y)
            similarities.append(s)
        
        doc = aligner.get_processed(lines_ru, lines_zh, sim_matrix, threshold, batch_number, batch_size)
        docs.append(doc)            
        
    pickle.dump(docs, open(processing_ru, "wb"))

    return {"items": {"ru": sentences_ru, "zh":sentences_zh, "sims": similarities}}

@app.route("/items/<username>/processing/<int:id_ru>/<int:count>/<int:page>", methods=["GET"])
def processing(username, id_ru, count, page):
    files_ru = helper.get_files_list(username, con.SPLITTED_FOLDER, con.RU_CODE)
    if len(files_ru) < id_ru+1:
        return EMPTY_SIMS
    processing_ru = os.path.join(con.UPLOAD_FOLDER, username, con.PROCESSING_FOLDER, con.RU_CODE, files_ru[id_ru])
    docs = pickle.load(open(processing_ru, "rb"))
    res = []
    lines_count = 0    
    shift = (page-1)*count
    for doc in docs:
        for line in doc:
            lines_count += 1
            if count>0 and (lines_count<=shift or lines_count>shift+count):
                continue
            #selected — x[2] is selected translation candidate
            selected = next((x for x in doc[line] if x[2]==1), (DocLine([],""), 0))
            #print(selected)
            res.append({
                "text": line.text,
                "line_ids": line.line_ids,
                "trans": [{
                    "text": t[0].text, 
                    "line_ids":t[0].line_ids, 
                    "sim": t[1]
                    } for t in doc[line]],
                "selected": {
                    "text": selected[0].text, 
                    "line_ids":selected[0].line_ids, 
                    "sim": selected[1]
                    }})
    total_pages = (lines_count//count) + (1 if lines_count%count != 0 else 0)
    meta = {"page": page, "total_pages": total_pages}
    return {"items": res, "meta": meta}

if __name__ == "__main__":
    app.run(port=12000, debug=True)
