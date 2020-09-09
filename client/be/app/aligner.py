import logging
import pickle
from typing import List

import matplotlib
import numpy as np
import seaborn as sns
#https://stackoverflow.com/questions/49921721/runtimeerror-main-thread-is-not-in-main-loop-with-matplotlib-and-flask
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from scipy import spatial

import config
import helper
import model_dispatcher
import sim_helper



def serialize_docs(lines_from, lines_to, processing_from_to, res_img, res_img_best, lang_name_from, lang_name_to, threshold=config.DEFAULT_TRESHOLD, batch_size=config.DEFAULT_BATCHSIZE):
    batch_number = 1
    docs = []
    vectors1 = []
    vectors2 = []
    zero_treshold = 0

    logging.debug(f"Aligning started.")
    for lines_from_batch, lines_from_proxy_batch, lines_to_batch in helper.get_batch(lines_from, lines_to, lines_to, batch_size):
        print("batch:", batch_number)
        logging.debug(f"Batch {batch_number}. Calculating vectors.")
        vectors1 = [*vectors1, *get_line_vectors(lines_from_batch)]
        vectors2 = [*vectors2, *get_line_vectors(lines_to_batch)]
        batch_number += 1
        logging.debug(f"Batch {batch_number}. Vectors calculated. len(vectors1)={len(vectors1)}. len(vectors2)={len(vectors2)}.")

        #test version restriction
        break
    
    logging.debug(f"Calculating similarity matrix.")
    sim_matrix = get_sim_matrix(vectors1, vectors2)
    sim_matrix_best = sim_helper.best_per_row(sim_matrix)

    sim_matrix_best = sim_helper.fix_inside_window(sim_matrix, sim_matrix_best, window_size=2)

    # res_ru, res_zh, res_ru_proxy, sims = get_pairs(lines_from, lines_to, lines_to, sim_matrix, threshold)
    
    plt.figure(figsize=(16,16))
    sns.heatmap(sim_matrix, cmap="Greens", vmin=zero_treshold, cbar=False)
    plt.savefig(res_img, bbox_inches="tight")

    plt.figure(figsize=(16,16))
    sns.heatmap(sim_matrix_best, cmap="Greens", vmin=zero_treshold, cbar=False)
    plt.xlabel(lang_name_to, fontsize=18)
    plt.ylabel(lang_name_from, fontsize=18)
    plt.savefig(res_img_best, bbox_inches="tight")

    logging.debug(f"Processing lines.")
    doc = get_processed(lines_from, lines_to, sim_matrix, zero_treshold, batch_number, batch_size)
    docs.append(doc)
    
    logging.debug(f"Dumping to file {processing_from_to}.")
    pickle.dump(docs, open(processing_from_to, "wb"))

def get_line_vectors(lines):
    return model_dispatcher.models[config.MODEL].embed(lines)

def get_processed(lines_from, lines_to, sim_matrix, threshold, batch_number, batch_size, candidates_count=50):
    doc = {}
    for line_from_id in range(sim_matrix.shape[0]):
        line = DocLine([line_from_id], lines_from[line_from_id])
        doc[line] = {
            "trn": (DocLine(0), 0.0 ,False),     #translation (best from candidates)
            "cnd": []      #all candidates
            }
        candidates = []
        for line_to_id in range(sim_matrix.shape[1]):            
            if sim_matrix[line_from_id, line_to_id] > threshold:
                candidates.append((line_to_id, sim_matrix[line_from_id, line_to_id]))

        for i,c in enumerate(sorted(candidates, key=lambda x: x[1], reverse=True)[:candidates_count]):
            if i==0:
                print(doc[line])
                doc[line]["trn"] = (DocLine(c[0], lines_to[c[0]]), sim_matrix[line_from_id, c[0]], False)
            doc[line]["cnd"].append(
                (
                    #text with line_id
                    DocLine(
                        line_id = c[0],
                        text = lines_to[c[0]]),
                    #text similarity
                    sim_matrix[line_from_id, c[0]])
                )
    return doc

def get_pairs(lines_from, lines_to, ru_proxy_lines, sim_matrix, threshold):
    res_from = []
    res_to = []
    proxy_from = []
    sims = []
    for i in range(sim_matrix.shape[0]):
        for j in range(sim_matrix.shape[1]):
            if sim_matrix[i,j] >= threshold:
                res_from.append(lines_from[j])
                res_to.append(lines_to[i])
                proxy_from.append(ru_proxy_lines[i])
                sims.append(sim_matrix[i,j])
                
    return res_from,res_to,proxy_from,sims

def get_sim_matrix(vec1, vec2, window=config.DEFAULT_WINDOW):
    sim_matrix = np.zeros((len(vec1), len(vec2)))
    k = len(vec1)/len(vec2)
    for i in range(len(vec1)):
        for j in range(len(vec2)):
            if (j*k > i-window) & (j*k < i+window):
                sim = 1 - spatial.distance.cosine(vec1[i], vec2[j])
                sim_matrix[i,j] = max(sim, 0.01)
    return sim_matrix

class DocLine:
    def __init__(self, line_id:int, text=None):
        self.line_id = line_id
        self.text = text
    def __hash__(self):
        return hash(str(self.line_id))
    def __eq__(self, other):
        return self.text == other
