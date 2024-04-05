import logging

import numpy as np
import torch
from torch import nn
from torcheval.metrics import BinaryF1Score
from tqdm import tqdm
from transformers import AdamW, get_linear_schedule_with_warmup

from src.settings import LoggerSettings
from src.utils.model_helpers import EarlyStopping

logger = logging.getLogger(LoggerSettings().logger_name)


def train_module(
    model: torch.nn.Module,
    device: torch.device,
    train_dataloader: torch.utils.data.DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: torch.nn.Module,
    metric,
    scheduler,
    train_losses: list,
    train_metrics: list,
):
    """Trains the model for one epoch using the training dataloader."""
    # setting model to train mode
    model.train()
    pbar = tqdm(train_dataloader, desc="Training", colour="green")

    # batch metrics
    train_loss = 0
    train_metric = 0
    processed_batch = 0

    for _, data in enumerate(pbar):

        ids = data["input_ids"].to(device)
        mask = data["attention_mask"].to(device)
        targets = data["targets"].to(device)

        # logger.info(f"The target shape is {targets.shape}")

        # model output
        outputs = model(ids, mask)
        outputs = outputs.flatten()
        # logger.info(f"The output shape is {outputs.shape}")

        # calc loss
        loss = criterion(outputs, targets)
        train_loss += loss.item()
        # logger.info(f"training loss for batch {idx} is {loss}")

        # backpropagation
        optimizer.zero_grad()  # flush out  existing grads
        loss.backward()  # back prop of weights wrt loss
        
        # gradient clipping -- prevent gradient explosion
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        # improvement steps
        optimizer.step()  # optimizer step -> minima
        if scheduler is not None:
            scheduler.step()  # scheduler step -> lr scheduling

        # metric calc
        metric.update(outputs, targets)
        train_metric += metric.compute().detach().item()

        # updating batch count
        processed_batch += 1

        pbar.set_description(
            f"Avg Train Loss: {train_loss/processed_batch} Avg Train Metric: {train_metric/processed_batch}"
        )

    # It's typically called after the epoch completes
    metric.reset()
    # updating epoch metrics
    train_losses.append(train_loss / processed_batch)
    train_metrics.append(train_metric / processed_batch)

    return train_losses, train_metrics


def test_module(
    model: torch.nn.Module,
    device: torch.device,
    test_dataloader: torch.utils.data.DataLoader,
    criterion: torch.nn.Module,
    metric,
    test_losses,
    test_metrics,
):
    """Tests the model for one epoch using the test dataloader."""
    # setting model to eval mode
    model.eval()
    pbar = tqdm(test_dataloader, desc="Testing", colour="blue")

    # batch metrics
    test_loss = 0
    test_metric = 0
    processed_batch = 0

    with torch.inference_mode():
        for _, data in enumerate(pbar, 0):
            ids = data["input_ids"].to(device)
            mask = data["attention_mask"].to(device)
            targets = data["targets"].to(device)

            # logger.info(f"The target shape is {targets.shape}")

            # model output
            outputs = model(ids, mask)
            outputs = outputs.flatten()

            # logger.info(f"The output shape is {outputs.shape}")

            # calc loss
            loss = criterion(outputs, targets)
            test_loss += loss.item()

            # metric calc
            metric.update(outputs, targets)
            test_metric += metric.compute().detach().item()

            # updating batch count
            processed_batch += 1

            pbar.set_description(
                f"Avg Test Loss: {test_loss/processed_batch} Avg Test Metric: {test_metric/processed_batch}"
            )

        # It's typically called after the epoch completes
        metric.reset()
        # updating epoch metrics
        test_losses.append(test_loss / processed_batch)
        test_metrics.append(test_metric / processed_batch)

    return test_losses, test_metrics


def training_drivers(
    model,
    learning_rate,
    train_loader,
    epochs,
    device,
    model_name,
):
    # loss
    criterion = torch.nn.BCEWithLogitsLoss()
    # optimizer
    optimizer = AdamW(model.parameters(), lr=learning_rate, correct_bias=False)
    # scheduler
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=total_steps
    )
    # metrics
    metric = BinaryF1Score(device=device)

    # early stopping
    early_stopping = EarlyStopping(patience=5, verbose=True, model_name=model_name)

    return criterion, optimizer, scheduler, metric, early_stopping


def get_predictions(model, data_loader, device, prob_thresh=0.7):
    """Returns the predictions and the real values"""
    review_texts = []
    predictions = []
    prediction_probs = []
    real_values = []

    model.eval()
    with torch.no_grad():
        for d in data_loader:
            texts = d["review_text"]
            input_ids = d["input_ids"].to(device)
            attention_mask = d["attention_mask"].to(device)
            targets = d["targets"].to(device)

            outputs = model(
                input_ids=input_ids, attention_mask=attention_mask
            ).flatten()

            probs = torch.sigmoid(outputs)

            preds = torch.where(
                probs > prob_thresh,
                torch.tensor(1.0).to(device),
                torch.tensor(0.0).to(device),
            )

            review_texts.extend(texts)
            predictions.extend(preds)
            prediction_probs.extend(probs)
            real_values.extend(targets)

    predictions = torch.stack(predictions).cpu().numpy()
    prediction_probs = np.round(torch.stack(prediction_probs).cpu().numpy(), 3)
    real_values = torch.stack(real_values).cpu().numpy()

    return review_texts, predictions, prediction_probs, real_values
