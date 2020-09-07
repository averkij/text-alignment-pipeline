import pickle
from aligner import DocLine

def save_tmx(input_file, output_file):
    docs = pickle.load(open(input_file, "rb"))
    with open(output_file, mode="w", encoding="utf-8") as doc_out:
        for doc in docs:
            for line in doc:
                selected = next((x for x in doc[line] if x[2]==1), (DocLine([],""), 0))
                if selected[0].text:
                    # if lang == lang_from:
                    doc_out.write(line.text)
                    # elif lang == lang_to:
                        # doc_out.write(selected[0].text)

def save_plain_text(input_file, output_file, first_lang):
    docs = pickle.load(open(input_file, "rb"))
    with open(output_file, mode="w", encoding="utf-8") as doc_out:
        for doc in docs:
            for line in doc:
                selected = next((x for x in doc[line] if x[2]==1), (DocLine([],""), 0))
                if selected[0].text:
                    if first_lang:
                        doc_out.write(line.text)
                    else:
                        doc_out.write(selected[0].text)