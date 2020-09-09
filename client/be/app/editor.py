import pickle
import constants as con

from aligner import DocLine

def edit_doc(edit_file, line_id, text, text_type=con.TYPE_TO):
    docs = pickle.load(open(edit_file, "rb"))
    line_to_find = DocLine(line_id)
    for doc in docs:
        if line_to_find in doc:
            if text_type == con.TYPE_TO:
                tr = doc[line_to_find]["trn"]
                doc[line_to_find]["trn"] = (DocLine(tr[0].line_id, text), tr[1], True) #IsEdited = True
            elif text_type == con.TYPE_FROM:
                pass
            else:
                raise Exception("Incorrect text type.")
            break

    pickle.dump(docs, open(edit_file, "wb"))