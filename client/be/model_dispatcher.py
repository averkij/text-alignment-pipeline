import os
import pickle

from sentence_transformers import SentenceTransformer

# model = SentenceTransformer('distiluse-base-multilingual-cased')
# pickle.dump(model, open("sentence_transformers.bin", 'wb'))

SENTENCE_TRANSFORMERS_MODEL_PATH = 'models/sentence_transformers.bin'

if os.path.isfile(SENTENCE_TRANSFORMERS_MODEL_PATH):
    sentence_transformers_model = pickle.load(open(SENTENCE_TRANSFORMERS_MODEL_PATH, 'rb'))
else:
    sentence_transformers_model = SentenceTransformer('distiluse-base-multilingual-cased')

models = {
    "sentence_transformer_multilang": sentence_transformers_model
}
