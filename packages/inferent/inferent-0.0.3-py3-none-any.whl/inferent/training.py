"""Utilities for model preprocessing, training, and testing"""

#TODO: convert to python3 syntax!

import copy
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.tensorboard import SummaryWriter

class DataManager:
    """Takes a pd.DataFrame as input and manages it for training.

    Performs preprocessing tasks.
    """

    logger = logging.getLogger("DataManager")
    raw_data = None
    data = None
    categorical_data = {}
    Xdf = None
    ydf = None
    Xdf_train = None
    Xdf_vld = None
    Xdf_test = None
    ydf_train = None
    ydf_vld = None
    ydf_test = None
    xscaler = None
    yscaler = None
    X_train = None
    X_vld = None
    X_test = None
    y_train = None
    y_vld = None
    y_test = None

    def __init__(self, raw_data, label_col, seed=None):
        self.raw_data = raw_data.copy()
        self.data = raw_data.copy()
        self.seed = seed
        self.label_col = label_col

    def drop_nans(self):
        """performs self.data.dropna() with some logging"""
        nan_cols = [
            col for col in self.data.columns if self.data[col].isna().sum() > 0
        ]
        nans = self.data[self.data[nan_cols].isna().any(axis=1)]
        self.logger.info(
            "%s rows of data with NaNs: %s \n %s", len(nans), nan_cols, nans
        )
        self.data = self.data.dropna()

    def add_categorical(self, cols, one_hot=True):
        """adds categorical cols `cols` to a separate datastore

        Will replace cols with their one hot encoded values
        """
        # TODO: embeddings
        for col in cols:
            cat = self.data[
                [col]
            ]  # double brackets to return dataframe rather than series
            if one_hot:
                ohe = OneHotEncoder()
                ohe.fit(cat)
                codes = ohe.transform(cat).toarray()
                feature_names = ohe.get_feature_names_out(cat.columns)
                cat = pd.DataFrame(
                    codes, columns=feature_names, index=cat.index
                ).astype(int)
                self.data = pd.concat(
                    [
                        self.data.drop(columns=[col]),
                        pd.DataFrame(
                            codes, columns=feature_names, index=cat.index
                        ).astype(int),
                    ],
                    axis=1,
                )
                self.categorical_data[col] = feature_names
            else:
                self.categorical_data[col] = col

    def split(
        self, vld_size=0.1, tst_size=0.1, vld_shuffle=True, tst_shuffle=False
    ):
        """Splits into train, test, and validation"""
        self.Xdf, self.ydf = (
            self.data.drop(columns=[self.label_col]),
            self.data[[self.label_col]],
        )
        Xdf_temp, self.Xdf_test, ydf_temp, self.ydf_test = train_test_split(
            self.Xdf,
            self.ydf,
            test_size=tst_size,
            random_state=self.seed,
            shuffle=tst_shuffle,
        )
        self.Xdf_train, self.Xdf_vld, self.ydf_train, self.ydf_vld = (
            train_test_split(
                Xdf_temp,
                ydf_temp,
                test_size=vld_size / (1.0 - tst_size),
                random_state=self.seed,
                shuffle=vld_shuffle,
            )
        )

    def normalize(self, scaler="minmax"):
        """normalizes data"""
        if scaler == "minmax":
            self.xscaler = MinMaxScaler()
            self.yscaler = MinMaxScaler()
        else:
            raise ValueError("Improper input for `scaler`.")

        self.X_train = self.xscaler.fit_transform(self.Xdf_train)
        self.X_vld = self.xscaler.transform(self.Xdf_vld)
        self.X_test = self.xscaler.transform(self.Xdf_test)
        self.y_train = self.yscaler.fit_transform(self.ydf_train)

        self.y_vld = self.yscaler.fit_transform(self.ydf_vld)
        self.y_test = self.yscaler.transform(self.ydf_test)

        # TODO: only for binary clasification
        self.logger.info(
            (
                self.ydf_vld.to_numpy() == self.yscaler.transform(self.ydf_vld)
            ).all()
        )  # sanity check :)
        self.logger.info(
            (
                self.ydf_test.to_numpy()
                == self.yscaler.transform(self.ydf_test)
            ).all()
        )  # sanity check :)

    def get_pytorch_trainloader(self, batch_size=64, shuffle=True):
        """Get TrainLoader"""
        # TODO: dtypes
        trainset = TensorDataset(
            torch.tensor(self.X_train, dtype=torch.float32),
            torch.tensor(self.y_train, dtype=torch.int),
        )
        return DataLoader(trainset, batch_size=batch_size, shuffle=shuffle)


class TorchModule(torch.nn.Module):
    """Pytorch module"""
    def __init__(self):
        super().__init__()
        # TODO: make this configurable by children
        self.install_hooks()

    def install_hooks(self, output=True):
        """Install hooks (configurable)"""
        if output:
            _ = torch.nn.modules.module.register_module_forward_hook(
                self.save_output_hook
            )

    def save_output_hook(self, module, _, output):
        """save any modules output in an attribute"""
        module.forward_output = output

    def forward(self):
        """forward"""
        raise NotImplementedError("forward not implemented")


class Trainer:
    """Model trainer class"""
    logger = logging.getLogger("Trainer")
    epoch = 0

    def __init__(
        self,
        name,
        datamgr,
        model,
        loss_fn,
        metrics,
        optimizer="adam",
        batch_size=64,
        max_epochs=50,
        lr=0.001,
    ):
        self.datamgr = datamgr
        self.model = model
        self.loss_fn = loss_fn
        self.metrics = metrics
        self.batch_size = batch_size
        self.max_epochs = max_epochs
        self.writer = SummaryWriter(name)
        if optimizer == "adam":
            self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        else:
            raise ValueError(f"Invalid optimizer {optimizer}")

    def write(self, name, x):
        """Write to summarywriter"""
        if x is None:
            self.logger.info("x is None. Not writing.")
            return
        if isinstance(x, torch.Tensor) and x.numel() > 1:
            self.writer.add_histogram(name, x, self.epoch)
        else:
            self.writer.add_scalar(
                name,
                x.item() if isinstance(x, torch.Tensor) else x,
                self.epoch,
            )

    def write_stdratio(self, name, x, y):
        """Write ratio of std to summarywriter"""
        if x is None or y is None:
            self.logger.info("x (%s) or y(%s) is None. Not writing.", x, y)
            return
        if isinstance(x, torch.Tensor) and x.numel() > 1:
            self.writer.add_histogram(name, x.std() / y.std(), self.epoch)
        else:
            self.writer.add_scalar(name, x.std() / y.std(), self.epoch)

    def train(self):
        """train"""
        self.logger.info(
            "Model has %s parameters", sum(x.reshape(-1).shape[0] for x in self.model.parameters())
        )
        batch_idx = 0

        trainloader = self.datamgr.get_pytorch_trainloader(
            batch_size=self.batch_size, shuffle=True
        )

        best_acc = np.inf  # init to negative infinity
        best_weights = None
        best_epoch = -1
        self.epoch = 0
        trn_metrics = copy.deepcopy(self.metrics)
        vld_metrics = copy.deepcopy(self.metrics)

        self.logger.info("Starting to train")
        for _ in range(self.max_epochs):
            trn_metrics.reset()
            vld_metrics.reset()
            for batch in trainloader:
                batch_idx += 1
                X, y = batch
                preds = self.model(X)
                metrics_output = trn_metrics.update(
                    preds.squeeze(), y.squeeze()
                )

                vld_preds = self.model(
                    torch.tensor(self.datamgr.X_vld, dtype=torch.float32)
                )
                vld_metrics_output = vld_metrics.update(
                    vld_preds.squeeze(),
                    torch.tensor(
                        self.datamgr.y_vld, dtype=torch.int
                    ).squeeze(),
                )

                loss_val = self.loss_fn(preds, y.type(torch.float32))
                self.optimizer.zero_grad()
                loss_val.backward()
                self.optimizer.step()

            for metric, metric_output in metrics_output.items():
                self.write(f"metrics/{metric}", metric_output[1])
            for metric, metric_output in vld_metrics_output.items():
                self.write(f"vld_metrics/{metric}", metric_output[1])
            # TODO: optimizer
            # self.model.write("learning_rate", optimizer.lr, scal=True)
            # logger.info(f"state_dict {optimizer.state_dict()}")

            moduledict = {}
            for name, module in self.model.named_modules():
                instancenum = moduledict.get(name, 0) + 1
                moduledict[name] = instancenum
                if isinstance(module, torch.nn.Linear):
                    self.write(f"linear{instancenum}/weights", module.weight)
                    self.write(
                        f"linear{instancenum}/weights/grad", module.weight.grad
                    )
                    self.write_stdratio(
                        f"linear{instancenum}/grad-data-ratio",
                        module.weight.grad,
                        module.weight,
                    )
                    self.write(f"linear{instancenum}/bias", module.bias)
                    self.write(
                        f"linear{instancenum}/bias/grad", module.bias.grad
                    )
                    self.write(
                        f"linear{instancenum}/output", module.forward_output
                    )
                elif isinstance(module, torch.nn.LayerNorm):
                    self.write(
                        f"layernorm{instancenum}/weights", module.weight
                    )
                    self.write(
                        f"layernorm{instancenum}/weights/grad",
                        module.weight.grad,
                    )
                    self.write(f"layernorm{instancenum}/bias", module.bias)
                    self.write(
                        f"layernorm{instancenum}/bias/grad", module.bias.grad
                    )
                    # TODO: check if output exists
                    self.write(
                        f"layernorm{instancenum}/output", module.forward_output
                    )

            def _get_metrics_str(metrics_output):
                return " | ".join(
                        [
                            metric + f" {metric_output[1]:,.2f}"
                            for metric, metric_output in metrics_output.items()
                        ]
                    )
            self.logger.info(
                "\033[33mEpoch %s, trn: %s \033[0m",
                self.epoch, _get_metrics_str(metrics_output)
            )
            self.logger.info(
                "\033[33mEpoch %s, vld: %s \033[0m",
                self.epoch, _get_metrics_str(vld_metrics_output)
            )
            if vld_metrics_output["Binary Cross Entropy"][1] < best_acc:
                best_acc = vld_metrics_output["Binary Cross Entropy"][1]
                best_weights = copy.deepcopy(self.model.state_dict())
                best_epoch = self.epoch
            self.epoch += 1

        self.logger.info(
            "Best model found in epoch %s with BCE %s.",
            best_epoch, best_acc
        )
        self.model.load_state_dict(best_weights)
