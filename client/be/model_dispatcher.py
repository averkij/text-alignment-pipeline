import pickle
from sentence_transformers import SentenceTransformer

# model = SentenceTransformer('distiluse-base-multilingual-cased')
# pickle.dump(model, open("sentence_transformers.bin", 'wb'))

models = {
    "sentence_transformer_multilang": pickle.load(open('models/sentence_transformers.bin', 'rb'))
}