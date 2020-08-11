import os
import pickle

import constants as con

# from models.use_multilingual_models import use_multilingual_v3_model
from models.sententense_transformers_models import sentence_transformers_model

models = {
    "sentence_transformer_multilingual": sentence_transformers_model,
    # "use_multilingual_v3": use_multilingual_v3_model
}
