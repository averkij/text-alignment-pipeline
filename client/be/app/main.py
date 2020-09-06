import datetime
import logging
import os
import pickle
import tempfile
import sys

from flask import Flask, abort, request, send_file
from flask_cors import CORS

import aligner
import constants as con
import helper
import splitter
from aligner import DocLine

#from mlflow import log_metric



app = Flask(__name__)
CORS(app)

#logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s [%(levelname)s] - %(process)d: %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# @app.route("/")
# def main():
#     index_path = os.path.join(app.static_folder, "index.html")
#     return send_file(index_path)

@app.route('/api/hello')
def start():
    return "Hallo, Welt."

@app.route("/items/<username>/raw/<lang>", methods=["GET", "POST"])
def items(username, lang):

    #TODO add language code validation

    helper.create_folders(username, lang)
    #load documents
    if request.method == "POST":
        if lang in request.files:
            file = request.files[lang]
            logging.debug(f"[{username}]. Loading lang document {file.filename}.")
            raw_path = os.path.join(con.UPLOAD_FOLDER, username, con.RAW_FOLDER, lang, file.filename)
            file.save(raw_path)
            splitter.split_to_sentences(file.filename, lang, username)
            logging.debug(f"[{username}]. Success. {file.filename} is loaded.")
        return {"res": 1}
    #return documents list
    files = {
        "items": {
            lang: helper.get_files_list(username, con.RAW_FOLDER, lang)
        }
    }
    return files

@app.route("/items/<username>/splitted/<lang>/<int:id>/download", methods=["GET"])
def download_splitted(username, lang, id):
    logging.debug(f"[{username}]. Downloading {lang} {id} splitted document.")
    files = helper.get_files_list(username, con.SPLITTED_FOLDER, lang)
    if len(files) < id+1:
        abort(404)
    path = os.path.join(con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang, files[id])
    if not os.path.isfile(path):
        logging.debug(f"[{username}]. Document not found.")
        abort(404)
    logging.debug(f"[{username}]. Document found. Path: {path}. Sent to user.")
    return send_file(path, as_attachment=True)  

@app.route("/items/<username>/splitted/<lang>/<int:id>/<int:count>/<int:page>", methods=["GET"])
def splitted(username, lang, id, count, page):
    files = helper.get_files_list(username, con.SPLITTED_FOLDER, lang)
    if len(files) < id+1:
        return con.EMPTY_LINES
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
        return con.EMPTY_LINES
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

@app.route("/items/<username>/align/<lang_from>/<lang_to>/<int:id_from>/<int:id_to>", methods=["GET"])
def align(username, lang_from, lang_to, id_from, id_to):
    files_from = helper.get_files_list(username, con.SPLITTED_FOLDER, lang_from)
    files_to = helper.get_files_list(username, con.SPLITTED_FOLDER, lang_to)
    if len(files_from) < id_from+1 or len(files_to) < id_to+1:
        logging.debug(f"[{username}]. Documents not found.")
        return con.EMPTY_SIMS
    
    logging.debug(f"[{username}]. Aligning documents. {files_from[id_from]}, {files_to[id_to]}.")
    processing_from = os.path.join(con.UPLOAD_FOLDER, username, con.PROCESSING_FOLDER, lang_from, files_from[id_from])
    res_img = os.path.join(con.STATIC_FOLDER, con.IMG_FOLDER, username, f"{files_from[id_from]}.png")
    res_img_best = os.path.join(con.STATIC_FOLDER, con.IMG_FOLDER, username, f"{files_from[id_from]}.best.png")
    splitted_from = os.path.join(con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang_from, files_from[id_from])
    splitted_to = os.path.join(con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang_to, files_to[id_to])
   
    logging.debug(f"[{username}]. Preparing for alignment. {splitted_from}, {splitted_to}.")
    with open(splitted_from, mode="r", encoding="utf-8") as input_from, \
         open(splitted_to, mode="r", encoding="utf-8") as input_to:
        #  ,open(ngramed_proxy_ru, mode="r", encoding="utf-8") as input_proxy:
        lines_from = input_from.readlines()
        lines_to = input_to.readlines()
        #lines_ru_proxy = input_proxy.readlines()

    aligner.serialize_docs(lines_from, lines_to, processing_from, res_img, res_img_best, lang_from, lang_to)
    return con.EMPTY_LINES

@app.route("/items/<username>/processing/<int:id_from>/<int:count>/<int:page>", methods=["GET"])
def processing(username, id_from, count, page):
    files_ru = helper.get_files_list(username, con.PROCESSING_FOLDER, con.RU_CODE)
    if len(files_ru) < id_from+1:
        return con.EMPTY_SIMS
    processing_ru = os.path.join(con.UPLOAD_FOLDER, username, con.PROCESSING_FOLDER, con.RU_CODE, files_ru[id_from])
    logging.debug(f"[{username}]. Get processing file. {processing_ru}.")
    if not os.path.isfile(processing_ru):
        abort(404)
        
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
                "line_id": line.line_id,
                "trans": [{
                    "text": t[0].text, 
                    "line_id":t[0].line_id, 
                    "sim": t[1]
                    } for t in doc[line]],
                "selected": {
                    "text": selected[0].text.strip(), 
                    "line_id":selected[0].line_id, 
                    "sim": selected[1]
                    }})
    total_pages = (lines_count//count) + (1 if lines_count%count != 0 else 0)
    meta = {"page": page, "total_pages": total_pages}
    return {"items": res, "meta": meta}

@app.route("/items/<username>/processing/<int:id_from>/<lang>/download", methods=["GET"])
def download_processsing(username, id_from, lang):
    logging.debug(f"[{username}]. Downloading {lang} {id_from} result document.")
    files_ru = helper.get_files_list(username, con.SPLITTED_FOLDER, con.RU_CODE)
    if len(files_ru) < id_from+1:
        logging.debug(f"[{username}]. Document {lang} with id={id_from} not found.")
        return con.EMPTY_SIMS
    processing_ru = os.path.join(con.UPLOAD_FOLDER, username, con.PROCESSING_FOLDER, con.RU_CODE, files_ru[id_from])
    if not os.path.isfile(processing_ru):
        logging.debug(f"[{username}]. Document {processing_ru} not found.")
        abort(404)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    processing_out = "{0}_{1}_{2}{3}".format(os.path.splitext(processing_ru)[0], lang, timestamp, os.path.splitext(processing_ru)[1])
    
    logging.debug(f"[{username}]. Preparing file for downloading {processing_out}.")
    docs = pickle.load(open(processing_ru, "rb"))
    with open(processing_out, mode="w", encoding="utf-8") as doc_out:        
        for doc in docs:
            for line in doc:
                selected = next((x for x in doc[line] if x[2]==1), (DocLine([],""), 0))
                if selected[0].text:
                    if lang == con.RU_CODE:
                        doc_out.write(line.text)
                    elif lang == con.ZH_CODE:
                        doc_out.write(selected[0].text)
    logging.debug(f"[{username}]. File {processing_out} prepared. Sent to user.")
    return send_file(processing_out, as_attachment=True)  

@app.route("/items/<username>/processing/list/<lang>", methods=["GET"])
def processing_list(username, lang):
    if not lang or lang != 'ru':
        logging.debug(f"[{username}]. Wrong language code: {lang}.")
        return con.EMPTY_FILES
    processing_folder = os.path.join(con.UPLOAD_FOLDER, username, con.PROCESSING_FOLDER, con.RU_CODE)
    if not os.path.isdir(processing_folder):
        return con.EMPTY_FILES        
    files = {
        "items": {
            lang: helper.get_files_list(username, con.PROCESSING_FOLDER, con.RU_CODE)
        }
    }
    return files

@app.route("/debug/items", methods=["GET"])
def show_items_tree():
    tree_path = os.path.join(tempfile.gettempdir(), "items_tree.txt")
    logging.debug(f"Temp file for tree structure: {tree_path}.")   
    with open(tree_path, mode="w", encoding="utf-8") as tree_out: 
        for root, dirs, files in os.walk(con.UPLOAD_FOLDER):
            level = root.replace(con.UPLOAD_FOLDER, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree_out.write(f"{indent}{os.path.basename(root)}" + "\n")
            subindent = ' ' * 4 * (level + 1)   
            for file in files:
                tree_out.write(f"{subindent}{file}" + "\n")
    return send_file(tree_path)

# Not API calls treated like static queries
@app.route("/<path:path>")
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, "index.html")
        return send_file(index_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
