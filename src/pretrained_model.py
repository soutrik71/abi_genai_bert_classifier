from transformers import BertModel, BertTokenizer

from src.settings import ModelSettings, TokenizerSettings

tokenizer = BertTokenizer.from_pretrained(TokenizerSettings().pretrained_model_name)
pretrained_model = BertModel.from_pretrained(ModelSettings().pretrained_model_name)
