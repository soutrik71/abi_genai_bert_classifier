import logging

from torch import nn
from transformers import BertModel

from src.settings import LoggerSettings

logger = logging.getLogger(LoggerSettings().logger_name)


class BertSentimentClassifier(nn.Module):
    """Basic Bert Binary Classifier"""

    def __init__(self, bert: BertModel, n_classes: int, dropout: float = 0.2):
        super(BertSentimentClassifier, self).__init__()
        self.bert = bert
        self.drop = nn.Dropout(p=dropout)
        self.classifier = nn.Linear(self.bert.config.hidden_size, n_classes)

    def forward(self, input_ids, attention_mask):

        model_op = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = model_op["pooler_output"]
        output = self.drop(pooled_output)
        return self.classifier(output)


class BertSentimentClassifierAdvanced(nn.Module):
    """Advanced Bert Binary Classifer with BatchNorm and FC layer"""

    def __init__(
        self,
        bert: BertModel,
        n_classes: int,
        fc_hidden: int = 64,
        dropout: float = 0.2,
    ):
        super(BertSentimentClassifierAdvanced, self).__init__()
        self.bert = bert
        self.drop = nn.Dropout(p=dropout)
        self.bn = nn.BatchNorm1d(self.bert.config.hidden_size)
        self.pooler = nn.Linear(self.bert.config.hidden_size, fc_hidden)
        self.classifier = nn.Linear(fc_hidden, n_classes)

    def forward(self, input_ids, attention_mask):

        model_op = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = model_op["pooler_output"]
        output = self.bn(pooled_output)
        output = self.drop(pooled_output)
        output = self.pooler(output)
        return self.classifier(output)
