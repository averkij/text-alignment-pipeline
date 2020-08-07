import os
import pickle

from sentence_transformers import SentenceTransformer

SENTENCE_TRANSFORMERS_MODEL_PATH = 'sentence_transformers.bin'

class SentenceTransformersModel():
    def __init__(self):        
        if os.path.isfile(SENTENCE_TRANSFORMERS_MODEL_PATH):
            print("Loading saved sentence_transformers model.")
            self.model = pickle.load(open(SENTENCE_TRANSFORMERS_MODEL_PATH, 'rb'))
        else:
            print("Loading sentence_transformers model from Internet.")
            self.model = SentenceTransformer('distiluse-base-multilingual-cased')      
    def embed(self, lines):
        vecs = self.model.encode(lines)
        return vecs

sentence_transformers_model = SentenceTransformersModel()

# model = SentenceTransformer('distiluse-base-multilingual-cased')
# pickle.dump(model, open("sentence_transformers.bin", 'wb'))
