import os
import constants as con

def get_files_list(username, folder, lang):
    if not os.path.isdir(os.path.join(con.UPLOAD_FOLDER, username, folder, lang)):
        return []
    return os.listdir(os.path.join(con.UPLOAD_FOLDER, username, folder, lang))

def create_folders(username):
    if not os.path.isdir(con.UPLOAD_FOLDER):
        os.mkdir(con.UPLOAD_FOLDER)
    if username and not os.path.isdir(os.path.join(con.UPLOAD_FOLDER, username)):
        os.mkdir(os.path.join(con.UPLOAD_FOLDER, username))
        create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.RAW_FOLDER))
        create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER))
        create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.PROXY_FOLDER))
        create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.NGRAM_FOLDER))
        create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.PROCESSING_FOLDER))
        create_subfolders(os.path.join(con.UPLOAD_FOLDER, username, con.DONE_FOLDER))

def create_subfolders(folder):
    os.mkdir(folder)
    os.mkdir(os.path.join(folder, con.RU_CODE))
    os.mkdir(os.path.join(folder, con.ZH_CODE))

def get_batch(iter1, iter2, iter3, n):
    l1 = len(iter1)
    l3 = len(iter3)
    k = int(round(n * l3/l1))    
    kdx = 0 - k
    for ndx in range(0, l1, n):
        kdx += k
        yield iter1[ndx:min(ndx + n, l1)], iter2[kdx:min(kdx + k, l3)], iter3[kdx:min(kdx + k, l3)]