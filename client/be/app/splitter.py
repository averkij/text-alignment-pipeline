import os
import re
import razdel

import constants as con

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

def split_zh(paragraph):
    for sent in re.findall(u'[^!?。！？\.\!\?]+[!?。！？\.\!\?]?', paragraph, flags=re.U):
        yield sent

def split_to_sentences(filename, langcode, username):
    raw = os.path.join(con.UPLOAD_FOLDER, username, con.RAW_FOLDER, langcode, filename)
    splitted = os.path.join(con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, langcode, filename)
    with open(raw, mode='r', encoding='utf-8') as input_file, open(splitted, mode='w', encoding='utf-8') as out_file:
        if langcode == con.RU_CODE:
            lines = ' '.join(input_file.readlines())
            lines = re.sub(pattern_ru_orig, '', lines)
            lines = re.sub(double_spaces, ' ', lines)
            lines = re.sub(double_commas, ',', lines)
            lines = re.sub(double_dash, '—', lines)
            sentences = list(x.text for x in razdel.sentenize(lines))
        elif langcode == con.ZH_CODE:
            lines = ''.join(input_file.readlines())

            #zh  
            lines = re.sub(pat_comma, '。', lines)
            sentences = list(re.sub(pattern_zh,'', x.strip()) for x in split_zh(lines))

            #de
            # lines = re.sub(double_spaces, ' ', lines)
            # lines = re.sub(double_commas, ',', lines)
            # lines = re.sub(double_dash, '—', lines)
            # sentences = list(x.text for x in razdel.sentenize(lines))
        else:
            raise Exception("Unknown language code.")
        
        count = 1
        for x in sentences:
            if count < len(sentences)-1:
                out_file.write(x.strip() + "\n")
            else:
                out_file.write(x.strip())
            count += 1
            #DEBUG
            #if count>50:
                #break