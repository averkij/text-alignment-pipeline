import os
import pickle

import tensorflow.compat.v2 as tf
import tensorflow_hub as hub

from tensorflow_text import SentencepieceTokenizer

USE_MULTILINGUAL_V3_MODEL_PATH = 'use_multilingual_v3.bin'

class UseMultilingualV3():
    def __init__(self):        
        if os.path.isfile(USE_MULTILINGUAL_V3_MODEL_PATH):
            self.model = pickle.load(open(USE_MULTILINGUAL_V3_MODEL_PATH, 'rb'))
        else:
            self.model = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual/3')      
    def embed(self, lines):
        vecs = self.model(lines).numpy()
        return vecs

use_multilingual_v3_model = UseMultilingualV3()


# use_multilingual_v3_model = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual/3')
# pickle.dump(use_multilingual_v3_model, open("use_multilingual_v3.bin", 'wb'))
