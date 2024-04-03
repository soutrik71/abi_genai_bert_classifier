import os
import random
import warnings

import matplotlib.pyplot as plt
import numpy as np
import torch

warnings.filterwarnings("ignore")


def set_seed(seed: int = 42) -> None:
    """Set seed for reproducibility"""
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    # When running on the CuDNN backend, two further options must be set
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    # Set a fixed value for the hash seed
    os.environ["PYTHONHASHSEED"] = str(seed)
    print(f"Random seed set as {seed}")


def plot_loss_accuracy(
    train_loss,
    val_loss,
    train_acc,
    val_acc,
    labels,
    colors,
    loss_legend_loc="upper center",
    acc_legend_loc="upper left",
    legend_font=5,
    fig_size=(16, 10),
    sub_plot1=(1, 2, 1),
    sub_plot2=(1, 2, 2),
):
    """Plot training and validation loss and accuracy"""

    plt.rcParams["figure.figsize"] = fig_size
    plt.figure

    plt.subplot(sub_plot1[0], sub_plot1[1], sub_plot1[2])

    for i in range(len(train_loss)):
        x_train = range(len(train_loss[i]))
        x_val = range(len(val_loss[i]))

        min_train_loss = np.array(train_loss[i]).min()

        min_val_loss = np.array(val_loss[i]).min()

        plt.plot(
            x_train,
            train_loss[i],
            linestyle="-",
            color="tab:{}".format(colors[i]),
            label="TRAIN ({0:.4}): {1}".format(min_train_loss, labels[i]),
        )
        plt.plot(
            x_val,
            val_loss[i],
            linestyle="--",
            color="tab:{}".format(colors[i]),
            label="VALID ({0:.4}): {1}".format(min_val_loss, labels[i]),
        )

    plt.xlabel("epoch no.")
    plt.ylabel("loss")
    plt.legend(loc=loss_legend_loc, prop={"size": legend_font})
    plt.title("Training and Validation Loss")

    plt.subplot(sub_plot2[0], sub_plot2[1], sub_plot2[2])

    for i in range(len(train_acc)):
        x_train = range(len(train_acc[i]))
        x_val = range(len(val_acc[i]))

        max_train_acc = np.array(train_acc[i]).max()

        max_val_acc = np.array(val_acc[i]).max()

        plt.plot(
            x_train,
            train_acc[i],
            linestyle="-",
            color="tab:{}".format(colors[i]),
            label="TRAIN ({0:.4}): {1}".format(max_train_acc, labels[i]),
        )
        plt.plot(
            x_val,
            val_acc[i],
            linestyle="--",
            color="tab:{}".format(colors[i]),
            label="VALID ({0:.4}): {1}".format(max_val_acc, labels[i]),
        )

    plt.xlabel("epoch no.")
    plt.ylabel("accuracy")
    plt.legend(loc=acc_legend_loc, prop={"size": legend_font})
    plt.title("Training and Validation Accuracy")

    plt.show()
    plt.close()


class EarlyStopping:
    """Early stops the training if validation loss doesn't improve after a given patience."""

    def __init__(
        self,
        patience=3,
        verbose=True,
        delta=1e-5,
        trace_func=print,
        path="models",
        model_name="model.pt",
    ):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement.
                            Default: False
            delta (float): Minimum change in the monitored quantity to qualify as an improvement.
                            Default: 0
            path (str): Path for the checkpoint to be saved to.
                            Default: 'checkpoint.pt'
            trace_func (function): trace print function.
                            Default: print
            path (str): Path for the checkpoint to be saved to.
                            Default: 'checkpoint.pt'
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta
        self.path = path
        self.model_name = model_name
        self.trace_func = trace_func

    def __call__(self, val_loss, model, epoch):

        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        elif score < self.best_score + self.delta:
            self.counter += 1
            self.trace_func(
                f"EarlyStopping counter: {self.counter} out of {self.patience}"
            )
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        """Saves model when validation loss decrease."""
        if self.verbose:
            self.trace_func(
                f"Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ..."
            )
        os.makedirs(self.path, exist_ok=True)
        torch.save(model.state_dict(), os.path.join(self.path, self.model_name))
        self.val_loss_min = val_loss


def get_device():
    """Get device (if GPU is available, use GPU)"""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
