import os
import pickle

import tensorflow.compat.v2 as tf
import tensorflow_hub as hub

from tensorflow_text import SentencepieceTokenizer

USE_MULTILINGUAL_V3_MODEL_PATH = './models/use_multilingual_models_saved/saved_model.pb'

class UseMultilingualV3():
    def __init__(self):        
        if os.path.isfile(USE_MULTILINGUAL_V3_MODEL_PATH):
            print("Loading saved use_multilingual_v3 model.")
            self.model = tf.saved_model.load("./models/use_multilingual_models_saved")
        else:
            print("Loading use_multilingual_v3 model from tf_hub.")
            self.model = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual/3')
            
    def embed(self, lines):
        vecs = self.model(lines).numpy()
        return vecs

use_multilingual_v3_model = UseMultilingualV3()

# use_multilingual_v3_model = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual/3')
# pickle.dump(use_multilingual_v3_model, open("use_multilingual_v3.bin", 'wb'))
