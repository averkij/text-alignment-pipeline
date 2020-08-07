import os
import pickle

from sentence_transformers import SentenceTransformer

import tensorflow_hub as hub

# model = SentenceTransformer('distiluse-base-multilingual-cased')
# pickle.dump(model, open("sentence_transformers.bin", 'wb'))

model = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual/3')
pickle.dump(model, open("use_multilingual_v3.bin", 'wb'))

SENTENCE_TRANSFORMERS_MODEL_PATH = 'models/sentence_transformers.bin'
USE_MULTILINGUAL_V3_MODEL_PATH = 'models/use_multilingual_v3.bin'

if os.path.isfile(SENTENCE_TRANSFORMERS_MODEL_PATH):
    sentence_transformers_model = pickle.load(open(SENTENCE_TRANSFORMERS_MODEL_PATH, 'rb'))
else:
    sentence_transformers_model = SentenceTransformer('distiluse-base-multilingual-cased')

if os.path.isfile(USE_MULTILINGUAL_V3_MODEL_PATH):
    use_multilingual_v3_model = pickle.load(open(USE_MULTILINGUAL_V3_MODEL_PATH, 'rb'))
else:
    use_multilingual_v3_model = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual/3')

models = {
    "sentence_transformer_multilingual": sentence_transformers_model,
    "use_multilingual_v3": use_multilingual_v3_model
}
