import pickle
from datetime import datetime

import helper
import output_templates
from aligner import DocLine


def save_tmx(input_file, output_file, lang_from, lang_to):
    tmx_template = output_templates.TMX_BLOCK.format(timestamp=datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'), \
        culture_from=helper.get_culture(lang_from), culture_to=helper.get_culture(lang_to))
    with open(output_file, mode="w", encoding="utf-8") as doc_out:
        for line_from, translation, candidates in helper.read_processing(input_file):
            doc_out.write(output_templates.TMX_BEGIN)
            if translation[0].text:
                doc_out.write(tmx_template.format(text_from=line_from.text.strip(), text_to=translation[0].text.strip()))
            doc_out.write(output_templates.TMX_END)

def save_plain_text(input_file, output_file, first_lang):
    with open(output_file, mode="w", encoding="utf-8") as doc_out:
        for line_from, translation, candidates in helper.read_processing(input_file):
            if translation[0].text:
                if first_lang:
                    doc_out.write(line_from.text)
                else:
                    doc_out.write(translation[0].text)
