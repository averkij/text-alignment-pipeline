import os
import constants as con

def get_files_list(username, folder, lang):
    if not os.path.isdir(os.path.join(con.UPLOAD_FOLDER, username, folder, lang)):
        return []
    return os.listdir(os.path.join(con.UPLOAD_FOLDER, username, folder, lang))

def create_folders(username, lang):
    if not os.path.isdir(con.UPLOAD_FOLDER):
        os.mkdir(con.UPLOAD_FOLDER)
    if not os.path.isdir(con.STATIC_FOLDER):
        os.mkdir(con.STATIC_FOLDER)
    if username and not os.path.isdir(os.path.join(con.STATIC_FOLDER, con.IMG_FOLDER, username)):
        create_img_folder(username)
    if username and not os.path.isdir(os.path.join(con.UPLOAD_FOLDER, username)):
        os.mkdir(os.path.join(con.UPLOAD_FOLDER, username))
    create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.RAW_FOLDER), lang)
    create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER), lang)
    create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.PROXY_FOLDER), lang)
    create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.NGRAM_FOLDER), lang)
    create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.PROCESSING_FOLDER), lang)
    create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.DONE_FOLDER), lang)
    #create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.IMG_FOLDER), lang)

def create_subfolders(folder, lang):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    if not os.path.isdir(os.path.join(folder, lang)):
        os.mkdir(os.path.join(folder, lang))

def create_img_folder(username):
    if not os.path.isdir(os.path.join(con.STATIC_FOLDER, con.IMG_FOLDER)):
        os.mkdir(os.path.join(con.STATIC_FOLDER, con.IMG_FOLDER))
    if username and not os.path.isdir(os.path.join(con.STATIC_FOLDER, con.IMG_FOLDER, username)):
        os.mkdir(os.path.join(con.STATIC_FOLDER, con.IMG_FOLDER, username))

def get_batch(iter1, iter2, iter3, n):
    l1 = len(iter1)
    l3 = len(iter3)
    k = int(round(n * l3/l1))    
    kdx = 0 - k
    for ndx in range(0, l1, n):
        kdx += k
        yield iter1[ndx:min(ndx + n, l1)], iter2[kdx:min(kdx + k, l3)], iter3[kdx:min(kdx + k, l3)]