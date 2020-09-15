import os
import pickle

from sentence_transformers import SentenceTransformer
import torch

# torch.backends.quantized.engine = 'qnnpack'

SENTENCE_TRANSFORMERS_MODEL_PATH = './models/sentence_transformers.bin'

class SentenceTransformersModel():
    def __init__(self):        
        if os.path.isfile(SENTENCE_TRANSFORMERS_MODEL_PATH):
            print("Loading saved sentence_transformers model.")
            # self.model = torch.quantization.quantize_dynamic(pickle.load(open(SENTENCE_TRANSFORMERS_MODEL_PATH, 'rb')), {torch.nn.Linear}, dtype=torch.qint8)
            self.model = pickle.load(open(SENTENCE_TRANSFORMERS_MODEL_PATH, 'rb'))
        else:
            print("Loading sentence_transformers model from Internet.")
            self.model = SentenceTransformer('distiluse-base-multilingual-cased')      
    def embed(self, lines):
        vecs = self.model.encode(lines)
        return vecs

sentence_transformers_model = SentenceTransformersModel()

###########model saving
# model = SentenceTransformer('distiluse-base-multilingual-cased')
# pickle.dump(model, open("sentence_transformers.bin", 'wb'))

############quantization

# import torch.quantization
# import torch

# model = SentenceTransformer('distiluse-base-multilingual-cased')

# quantized_model = torch.quantization.quantize_dynamic(
#     model, {torch.nn.Linear}, dtype=torch.qint8
# )
# print(quantized_model)

# torch.save(quantized_model.state_dict(), "sentence_transformers_q.bin")

#pruning
# from torch import nn
# import torch.nn.utils.prune as prune
# import torch.nn.functional as F

# model = SentenceTransformer('distiluse-base-multilingual-cased')

# parameters_to_prune = (
#     (model[0].bert.transformer.layer[0].ffn.lin1, 'weight'),
#     (model[0].bert.transformer.layer[0].ffn.lin2, 'weight'),
#     (model[0].bert.transformer.layer[1].ffn.lin1, 'weight'),
#     (model[0].bert.transformer.layer[1].ffn.lin2, 'weight'),
#     (model[0].bert.transformer.layer[2].ffn.lin1, 'weight'),
#     (model[0].bert.transformer.layer[2].ffn.lin2, 'weight'),
#     (model[0].bert.transformer.layer[3].ffn.lin1, 'weight'),
#     (model[0].bert.transformer.layer[3].ffn.lin2, 'weight'),
#     (model[0].bert.transformer.layer[4].ffn.lin1, 'weight'),
#     (model[0].bert.transformer.layer[4].ffn.lin2, 'weight'),
#     (model[0].bert.transformer.layer[5].ffn.lin1, 'weight'),
#     (model[0].bert.transformer.layer[5].ffn.lin2, 'weight'),
# )

# prune.global_unstructured(
#     parameters_to_prune,
#     pruning_method=prune.L1Unstructured,
#     amount=0.2,
# )

# for i in range(len(parameters_to_prune)):
#     prune.remove(parameters_to_prune[i][0], 'weight')

# # print(list(module.named_parameters()))
# torch.save(model.state_dict(), "sentence_transformers_p16.bin")
