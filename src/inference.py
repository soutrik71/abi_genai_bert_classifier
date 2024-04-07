import glob
import logging
import os
import warnings

import numpy as np
import torch

from src.dataloader import create_data_loader
from src.model import BertSentimentClassifier, BertSentimentClassifierAdvanced
from src.pretrained_model import pretrained_model, tokenizer
from src.settings import (
    AzureblobSettings,
    LoggerSettings,
    ModelSettings,
    TokenizerSettings,
)
from src.utils.model_helpers import get_device

warnings.filterwarnings("ignore")

logger = logging.getLogger(LoggerSettings().logger_name)


def saved_model_path(model_path=AzureblobSettings().input_path):
    file_paths = glob.glob(os.path.join(model_path, "*pt"))
    model_path_dict = {}

    for path in file_paths:
        if "advanced" in path:
            model_path_dict["advanced"] = path
        elif "base" in path:
            model_path_dict["base"] = path

    return model_path_dict


class ModelInference:
    def __init__(
        self,
        tokenizer=tokenizer,
        model_type="advanced",
        model=pretrained_model,
        max_len=TokenizerSettings().max_length,
        prob_thresh=ModelSettings().binary_thresh,
    ):
        self.device = get_device()
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.prob_thresh = prob_thresh
        model_path_dict = saved_model_path()

        # model declaration and loading with pretrained weights
        if model_type == "base":
            logger.info("Loading base model")
            self.bert_classifier = BertSentimentClassifier(
                bert=model,
                n_classes=ModelSettings().num_classes,
                dropout=ModelSettings().drop_out,
            )

            self.bert_classifier.load_state_dict(
                torch.load(f=model_path_dict["base"], map_location=self.device)
            )
            self.bert_classifier.to(self.device)

        elif model_type == "advanced":
            logger.info("Loading advanced model")
            self.bert_classifier = BertSentimentClassifierAdvanced(
                bert=model,
                n_classes=ModelSettings().num_classes,
                dropout=ModelSettings().drop_out,
            )
            self.bert_classifier.load_state_dict(
                torch.load(f=model_path_dict["advanced"], map_location=self.device)
            )
            self.bert_classifier.to(self.device)

    def _get_predictions(self, data_loader, model):
        """Returns only the predicted labels for the given data loader"""
        review_texts = []
        predictions = []
        prediction_probs = []

        model.eval()
        with torch.no_grad():
            for d in data_loader:
                texts = d["review_text"]
                input_ids = d["input_ids"].to(self.device)
                attention_mask = d["attention_mask"].to(self.device)

                outputs = model(
                    input_ids=input_ids, attention_mask=attention_mask
                ).flatten()

                probs = torch.sigmoid(outputs)

                preds = torch.where(
                    probs > self.prob_thresh,
                    torch.tensor(1.0).to(self.device),
                    torch.tensor(0.0).to(self.device),
                )

                review_texts.extend(texts)
                predictions.extend(preds)
                prediction_probs.extend(probs)

        predictions = torch.stack(predictions).cpu().numpy()
        prediction_probs = np.round(torch.stack(prediction_probs).cpu().numpy(), 3)

        return review_texts, predictions, prediction_probs

    def predict(self, user_query):
        """Returns the predicted labels for the given data loader"""
        logger.info(f"Predicting labels for query: {user_query}")
        query_loader = create_data_loader(
            question=[user_query],
            targets=None,
            max_len=self.max_len,
            batch_size=1,
            shuffle=False,
            tokenizer=tokenizer,
        )
        review_texts, predictions, prediction_probs = self._get_predictions(
            data_loader=query_loader,
            model=self.bert_classifier,
        )

        return dict(
            zip(
                review_texts,
                [
                    dict(
                        zip(
                            ["label", "prob"],
                            [predictions.tolist()[0], prediction_probs.tolist()[0]],
                        )
                    )
                ],
            )
        )
