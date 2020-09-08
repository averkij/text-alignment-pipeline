import pickle
from datetime import datetime

import helper
import output_templates
from aligner import DocLine


def save_tmx(input_file, output_file, lang_from, lang_to):
    docs = pickle.load(open(input_file, "rb"))
    tmx_template = output_templates.TMX_BLOCK.format(timestamp=datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'), \
        culture_from=helper.get_culture(lang_from), culture_to=helper.get_culture(lang_to))
    with open(output_file, mode="w", encoding="utf-8") as doc_out:
        doc_out.write(output_templates.TMX_BEGIN)
        for doc in docs:
            for line in doc:
                selected = next((x for x in doc[line] if x[2]==1), (DocLine([],""), 0))
                if selected[0].text:
                    doc_out.write(tmx_template.format(text_from=line.text.strip(), text_to=selected[0].text.strip()))
        doc_out.write(output_templates.TMX_END)

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
