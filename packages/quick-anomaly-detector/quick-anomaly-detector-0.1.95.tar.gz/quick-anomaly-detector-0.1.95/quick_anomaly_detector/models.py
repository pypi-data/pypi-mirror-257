import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from scipy.stats import multivariate_normal

import torch
import torch.nn as nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader, TensorDataset
import torch.optim as optim

import xgboost as xgb

import mlflow, datetime

#########################################
#   Gaussian Based Anomaly Detection    #
#########################################
# select epsilon base on F1
class AnomalyGaussianModel:
    """
    Anomaly Gaussian Model using Gaussian Distribution.

    This class provides a simple implementation of an anomaly detection model
    based on the Gaussian distribution. It includes methods for estimating
    Gaussian parameters, calculating p-values, selecting the threshold, and making predictions.

    Attributes:
        - **mu_train** (*ndarray*): Mean vector of the training data.
        - **var_train** (*ndarray*): Variance vector of the training data.
        - **p_values_train** (*ndarray*): P-values for training data.
        - **p_values_val** (*ndarray*): P-values for validation data.
        - **epsilon** (*float*): Chosen threshold for anomaly detection.
        - **f1** (*float*): F1 score corresponding to the chosen threshold.

    Example:

    .. code-block:: python

        from quick_anomaly_detector.models import AnomalyGaussianModel

        # Load your datasets (X_train, X_val, y_val)
        # ...

        # Create an instance of AnomalyGaussianModel
        model = AnomalyGaussianModel()

        # Train the model
        model.train(X_train, X_val, y_val)

        # Predict anomalies in the validation dataset
        anomalies = model.predict(X_val)

        print(anomalies)

    .. note::
        The anomaly detection model assumes that the input data follows a Gaussian distribution.

    .. warning::
        This class is designed for educational purposes and may not be suitable for all types of data.
    """

    def __init__(self, features=None, label=None):
        """
        Initialize the AnomalyDetectionModel.
        """
        self.mu_train = 0
        self.var_train = 0
        self.p_values_train = 0
        self.p_values_val = 0
        self.epsilon = 0.05
        self.f1 = 0
        self.trainset = None
        self.validset = None
        self.features = features
        self.label = label
    
    def estimate_gaussian(self, X):
        m, n = X.shape
        mu = np.mean(X, axis=0)
        var = np.var(X, axis=0)
        return mu, var
    
    def calculate_p_value(self, X, mu, var):
        mvn = multivariate_normal(mean=mu, cov=np.diag(var))
        p_values = mvn.pdf(X)
        return p_values
    
    def select_threshold(self, y_val, p_val): 
        best_epsilon = 0
        best_F1 = 0
        F1 = 0
        step_size = (max(p_val) - min(p_val)) / 1000
        for epsilon in np.arange(min(p_val), max(p_val), step_size):
            predictions = (p_val < epsilon).astype(int)
            tp = np.sum((predictions == 1) & (y_val == 1))
            fp = np.sum((predictions == 1) & (y_val == 0))
            fn = np.sum((predictions == 0) & (y_val == 1))
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            F1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            if F1 > best_F1:
                best_F1 = F1
                best_epsilon = epsilon
        return best_epsilon, best_F1
   
    def train(self, train_df, valid_df, features=None, label=None):
        """
        Train the AnomalyDetectionModel.

            :param X_train: Training data matrix.
            :type X_train: ndarray

            :param X_val: Validation data matrix.
            :type X_val: ndarray

            :param y_val: Ground truth labels for validation data.
            :type y_val: ndarray
        """
        if features is not None:
            self.features = features
        if label is not None:
            self.label = label
        self.trainset = train_df
        self.validset = valid_df
        X_train = train_df[self.features].values
        X_val = valid_df[self.features].values
        y_val = valid_df[self.label].values
        self.mu_train, self.var_train = self.estimate_gaussian(X_train)
        self.p_values_train = self.calculate_p_value(X_train, self.mu_train, self.var_train)
        self.p_values_val = self.calculate_p_value(X_val, self.mu_train, self.var_train)
        self.epsilon, self.f1 = self.select_threshold(y_val, self.p_values_val)

    def predict(self, X):
        """
        Predict outliers in the input data.

        Parameters:
            :param X: Input data matrix.
            :type X: ndarray

        Returns:
            :return: Boolean array indicating whether each sample is an outlier.
            :rtype: ndarray
        """
        X_ = X[self.features]
        p_values = self.calculate_p_value(X_, self.mu_train, self.var_train)
        outliers = p_values < self.epsilon
        return outliers
  
    def log_model(self, model_uri, experiment_id=0, r_name = "run", metrics={}, registered_model_name = None):
        """
        If you need credential, make sure you have them in your environment:   

        .. code-block:: python

            os.environ['AWS_ACCESS_KEY_ID'] = os.environ.get("AWS_ACCESS_KEY_ID")
            os.environ['AWS_SECRET_ACCESS_KEY'] = os.environ.get("AWS_SECRET_ACCESS_KEY")
            os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'https://<endpoint>.<domain>.com'
            os.environ['MLFLOW_S3_BUCKET'] = 'bucketname'
        """
        try:
            mlflow.set_tracking_uri(model_uri)
            mlflow.set_experiment(experiment_id)
            now = datetime.datetime.now()
            with mlflow.start_run(experiment_id=experiment_id, run_name=f"{r_name}_{now}") as run:
                trainset = mlflow.data.from_pandas(self.trainset)
                validset = mlflow.data.from_pandas(self.validset)
                mlflow.log_input(trainset, context="trainset")
                mlflow.log_input(validset, context="validset")
                for metric_name, metric_value in metrics.items():
                    if isinstance(metric_value, (int, float)):
                        mlflow.log_metric(metric_name, metric_value)
                mlflow.log_param("mu", self.mu_train)
                mlflow.log_param("var", self.var_train)
                mlflow.log_param("epsilon", self.epsilon)
                # mlflow.pyfunc.log_model(artifact_path="", python_model=self.predict)
                mlflow.end_run()
            return True
        except Exception as e:
            raise e




#########################################
#      NN Based Anomaly Detection       #
#########################################
class AnomalyDetectionNN(nn.Module):
    """
    AnomalyDetectionNN is a neural network model designed for anomaly detection tasks.

    It consists of three fully connected layers:
    - Input layer: Takes input data with a shape of (batch_size, input_dim).
    - Hidden layer 1: Consists of 64 neurons and applies ReLU activation function.
    - Hidden layer 2: Consists of 32 neurons and applies ReLU activation function.
    - Output layer: Consists of input_dim neurons, representing the reconstructed data.
      It applies the sigmoid activation function to squash the output values between 0 and 1.

    Parameters:
        input_dim (int): The number of features in the input data.

    Attributes:
        fc1 (nn.Linear): The first fully connected layer.
        fc2 (nn.Linear): The second fully connected layer.
        fc3 (nn.Linear): The output layer.

    Methods:
        forward(x): Forward pass through the neural network.
    
    Example:

    .. code-block:: python

        from quick_anomaly_detector.models import AnomalyDetectionNN

        # Load your datasets (X_train, X_val)
        # ...
        
        # normalization
        min_vals = np.min(X_train, axis=0)
        max_vals = np.max(X_train, axis=0)
        normalized_training_data = (X_train - min_vals) / (max_vals - min_vals)
        normalized_validation_data = (X_valid - min_vals) / (max_vals - min_vals)
        input_dim = normalized_training_data.shape[1]

        # Create an instance of AnomalyDetectionModel
        model = AnomalyDetectionNN(input_dim)

        # Train the model
        X_train_tensor = torch.tensor(normalized_training_data, dtype=torch.float32)
        train_dataset = TensorDataset(X_train_tensor)
        train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

        X_valid_tensor = torch.tensor(normalized_validation_data, dtype=torch.float32)
        valid_dataset = TensorDataset(X_valid_tensor)
        valid_loader = DataLoader(valid_dataset, batch_size=64, shuffle=False)

        optimizer = optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.MSELoss()
        # train ...


    """
    def __init__(self, input_dim, min_vals = None, max_vals = None):
        """
        Initialize the AnomalyDetectionNN model.

        Args:
            input_dim (int): The number of features in the input data.
            min_vals (list): Min values of each feature in train data.
            max_vals (list): Max values of each feature in train data.
        """
        super(AnomalyDetectionNN, self).__init__()
        self.min_vals = min_vals
        self.max_vals = max_vals
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, input_dim)  # same as input, for loss calculation

    def forward(self, x):
        """
        Perform the forward pass through the neural network.

        Args:
            x (torch.Tensor): The input data tensor with shape (batch_size, input_dim).

        Returns:
            torch.Tensor: The reconstructed output tensor with the same shape as the input.
        """
        x = self.fc1(x)   # input shape is (1, N, M), N is samples number, M is feaures number
        x = torch.relu(x)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)
        x = torch.sigmoid(x)  # Apply sigmoid activation to squash output between 0 and 1
        return x
    

################################################
#          Train Anomaly NN model              #
################################################
class TrainAnomalyNN:
    """
    Class for training and using an anomaly detection neural network.

    Attributes:
    
    :param lr: The learning rate for optimization (default: 0.001).
    :type lr: float

    :param num_epochs: The maximum number of training epochs (default: 1000).
    :type num_epochs: int

    :param patience: The number of epochs to wait before early stopping if validation loss does not improve (default: 10).
    :type patience: int

    :param model: The trained anomaly detection neural network model.
    :type model: AnomalyDetectionNN

    :param optimizer: The optimizer used for training.
    :type optimizer: torch.optim.Optimizer

    :param criterion: The loss function used for training.
    :type criterion: torch.nn.Module

    :param train_loss_arr: The training loss array.
    :type train_loss_arr: numpy.ndarray

    :param valid_loss_arr: The validation loss array.
    :type valid_loss_arr: numpy.ndarray

    :param train_min_values: The minimum values of each feature in the training dataset.
    :type train_min_values: numpy.ndarray

    :param train_max_values: The maximum values of each feature in the training dataset.
    :type train_max_values: numpy.ndarray

    Example:
    
    .. code-block:: python

        from quick_anomaly_detector.models import TrainAnomalyNN

        train_model = TrainAnomalyNN(lr=0.001, num_epochs=1000, patience=10)
        train_model.train(X_train, X_valid)
        predict_result = train_model.predict(X_valid, threshold = 0.0002)

    """
    def __init__(self, lr=0.001, num_epochs=1000, patience=10):
        """
        Initializes the TrainAnomalyNN class.

        Args:
        - lr (float): The learning rate for optimization (default: 0.001).
        - num_epochs (int): The maximum number of training epochs (default: 1000).
        - patience (int): The number of epochs to wait before early stopping if validation loss does not improve (default: 10).
        """
        self.input_dim = None
        self.lr = lr
        self.num_epochs = num_epochs
        self.patience = patience
        self.model = None
        self.optimizer = None
        self.criterion = None
        self.stop_step = 0
        self.best_loss = 0
        self.train_loss_arr = []
        self.valid_loss_arr = []
        self.train_min_values = None
        self.train_max_values = None
        self.trainset = None
        self.validset = None
        self.features = None
    
    def _normalize_data(self, X, isValid=False):
        """Normalizes the input data."""
        if isValid:
            min_vals = self.train_min_values
            max_vals = self.train_max_values
        else:
            min_vals = np.min(X, axis=0)
            max_vals = np.max(X, axis=0)
            self.train_min_values = min_vals
            self.train_max_values = max_vals
        normalized_data = (X - min_vals) / (max_vals - min_vals)
        return normalized_data
    
    def train(self, train_df, valid_df, features = None):
        """
        Trains the anomaly detection neural network.

        Args:
        - X_train (numpy.ndarray): The training data.
        - X_valid (numpy.ndarray): The validation data.
        """
        self.trainset = train_df
        self.validset = valid_df
        if features is not None:
            self.features = features
        X_train = train_df[self.features].values
        X_valid = valid_df[self.features].values
        # Normalize training and validation data
        normalized_training_data = self._normalize_data(X_train)
        normalized_validation_data = self._normalize_data(X_valid, True)
        # Convert data to PyTorch tensors
        train_dataset = TensorDataset(torch.tensor(normalized_training_data, dtype=torch.float32))
        train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
        valid_dataset = TensorDataset(torch.tensor(normalized_validation_data, dtype=torch.float32))
        valid_loader = DataLoader(valid_dataset, batch_size=64, shuffle=False)
        # Initialize model, optimizer, and loss function
        input_dim = normalized_training_data.shape[1]
        self.input_dim = input_dim
        self.model = AnomalyDetectionNN(self.input_dim, self.train_min_values, self.train_max_values)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        best_loss = float('inf')
        counter = 0
        for epoch in range(self.num_epochs):
            self.model.train()
            running_loss = 0.0
            for batch_inputs in train_loader:
                self.optimizer.zero_grad()
                for inputs in batch_inputs:  # Iterate over each tensor in the batch
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs, inputs)  # Reconstruction loss (MSE)
                    loss.backward()
                    self.optimizer.step()
                    running_loss += loss.item() * inputs.size(0)
            epoch_loss = running_loss / len(train_loader.dataset)
            self.train_loss_arr.append(epoch_loss)
            # print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {epoch_loss:.4f}") # traning loss
            # Evaluate validation loss
            self.model.eval()
            with torch.no_grad():
                valid_loss = 0.0
                for valid_inputs in valid_loader:
                    for inputs in valid_inputs:
                        outputs = self.model(inputs)
                        loss = self.criterion(outputs, inputs)
                        valid_loss += loss.item() * inputs.size(0)
                valid_loss /= len(valid_loader.dataset)
                self.valid_loss_arr.append(valid_loss)
            if valid_loss < best_loss:
                best_loss = valid_loss
                counter = 0
            else:
                counter += 1
            if counter >= self.patience:
                self.stop_step = epoch
                self.best_loss = best_loss
                # print("Validation loss has not improved for {} epochs. Early stopping.".format(patience))
                break
    
    def predict(self, X, threshold = 0.0002):
        """
        Predicts anomalies in the input data.

        Args:
        - X (numpy.ndarray): The input data.
        - threshold (float): The threshold for anomaly detection (default: 0.0002).

        Returns:
        - predictions (torch.Tensor): Tensor containing the predictions (1 for anomaly, 0 for normal) for each input sample.
        - reconstruction_loss: Tensor containing the loss of reconstructed_data
        """
        X_ = X[self.features].values
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        with torch.no_grad():
            normalized_data = self._normalize_data(X_, True)
            X_tensor = torch.tensor(normalized_data, dtype=torch.float32)
            self.model.eval()
            reconstructed_data = self.model(X_tensor)
            reconstruction_loss = torch.mean(torch.square(X_tensor - reconstructed_data), dim=1)
            predictions = (reconstruction_loss > threshold).int()
        return predictions, reconstruction_loss

    def log_model(self, model_uri, experiment_id=0, r_name = "run", metrics={}, registered_model_name = None):
        """
        If you need credential, make sure you have them in your environment:   

        .. code-block:: python

            os.environ['AWS_ACCESS_KEY_ID'] = os.environ.get("AWS_ACCESS_KEY_ID")
            os.environ['AWS_SECRET_ACCESS_KEY'] = os.environ.get("AWS_SECRET_ACCESS_KEY")
            os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'https://<endpoint>.<domain>.com'
            os.environ['MLFLOW_S3_BUCKET'] = 'bucketname'
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        try:
            mlflow.set_tracking_uri(model_uri)
            mlflow.set_experiment(experiment_id)
            now = datetime.datetime.now()
            with mlflow.start_run(experiment_id=experiment_id, run_name=f"{r_name}_{now}") as run:
                trainset = mlflow.data.from_pandas(self.trainset)
                validset = mlflow.data.from_pandas(self.validset)
                mlflow.log_input(trainset, context="trainset")
                mlflow.log_input(validset, context="validset")
                for metric_name, metric_value in metrics.items():
                    if isinstance(metric_value, (int, float)):
                        mlflow.log_metric(metric_name, metric_value)
                mlflow.log_param("input_dim", self.input_dim)
                mlflow.log_param("lr", self.lr)
                mlflow.log_param("stop_step", self.stop_step)
                mlflow.log_param("best_loss", self.best_loss)
                mlflow.log_param("train_min_values", self.train_min_values)
                mlflow.log_param("train_max_values", self.train_max_values)
                mlflow.log_param("features", self.features)
                if registered_model_name is None:
                    mlflow.pytorch.log_model(pytorch_model=self.model, artifact_path="AnomalyNN")
                else:
                    mlflow.pytorch.log_model(artifact_path="AnomalyNN", pytorch_model=self.model, registered_model_name = registered_model_name)
                mlflow.end_run()
            return True
        except Exception as e:
            raise e






#########################################
#           Embedding NN model          #
#########################################
import torch, math
from torch import nn, Tensor
from torch.nn import TransformerEncoder, TransformerEncoderLayer
class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)
    def forward(self, x: Tensor) -> Tensor:
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)  

class TransformerModel(nn.Module):
    """
    This is letter level embedding NN model
    """
    def __init__(self, ntoken: int, d_model: int, nhead: int, d_hid: int,
                 nlayers: int, dropout: float = 0.5, sequence_length = 38):
        super().__init__()
        self.model_type = 'Transformer'
        self.pos_encoder = PositionalEncoding(d_model, dropout)
        encoder_layers = TransformerEncoderLayer(d_model, nhead, d_hid, dropout)
        self.transformer_encoder = TransformerEncoder(encoder_layers, nlayers)
        self.embedding = nn.Embedding(ntoken, d_model)
        self.d_model = d_model
        self.linear = nn.Linear(d_model * sequence_length, 2) # self.linear = nn.Linear(d_model * sequence_length, 3)
        # self.softmax = nn.Softmax(dim=1)  # Add softmax activation
        self.init_weights()

    def init_weights(self) -> None:
        initrange = 0.1
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.linear.bias.data.zero_()
        self.linear.weight.data.uniform_(-initrange, initrange)

    def forward(self, src: Tensor, src_mask: Tensor = None) -> Tensor:
        src = self.embedding(src) * math.sqrt(self.d_model)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src, src_mask)
        B, _, _ = output.shape
        output = output.reshape(B, -1)
        output = self.linear(output) # B ,S * D
        # probabilities = self.softmax(output)
        return output

class TrainEmbedding:
    def __init__(self, lr=0.001, num_epochs=1000, patience=10, batch_size=32, 
                 embedding_dim = 4, nhead = 8, d_hid=64, nlayers = 2, dropout = 0.5):
        self.lr = lr
        self.num_epochs = num_epochs
        self.patience = patience
        self.model = None
        self.optimizer = None
        self.criterion = None
        self.letter_to_number = {'a': 1,  'b': 2,  'c': 3,  'd': 4,  'e': 5,  'f': 6,  'g': 7,  'h': 8,  'i': 9,  'j': 10,
            'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 
            'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26, 
            'A': 27, 'B': 28, 'C': 29, 'D': 30, 'E': 31, 'F': 32, 'G': 33, 'H': 34, 'I': 35, 'J': 36, 
            'K': 37, 'L': 38, 'M': 39, 'N': 40, 'O': 41, 'P': 42, 'Q': 43, 'R': 44, 'S': 45, 'T': 46, 
            'U': 47, 'V': 48, 'W': 49, 'X': 50, 'Y': 51, 'Z': 52, 
            '0': 53, '1': 54, '2': 55, '3': 56, '4': 57, '5': 58, '6': 59, '7': 60, '8': 61, '9': 62,
            '.': 63, '-': 64, ' ': 65, '@': 66, '?': 67, '/': 68,  "'": 69, "|": 70, 
            '+': 71, 'â': 72}
        self.max_length = 0
        self.batch_size = batch_size
        self.vocab_size = len(self.letter_to_number)+1
        self.embedding_dim = embedding_dim
        self.nhead = nhead
        self.d_hid = d_hid
        self.nlayers = nlayers
        self.dropout = dropout
        self.stop_step = 0
        self.best_loss = np.inf
        self.train_loss_arr = []
        self.valid_loss_arr = []
        self.feature_name = None
        self.label_name = None
        self.trainset = None
        self.validset = None

    def get_encode(self, x):
        encoded_name = [self.letter_to_number[letter] for letter in x if letter in self.letter_to_number]
        return encoded_name
    def padding(self, sequences, max_length):
        for i in range(len(sequences)):
            if len(sequences[i]) < max_length:
                sequences[i] = sequences[i] + [0] * (max_length - len(sequences[i]))
            elif len(sequences[i]) > max_length:
                sequences[i] = sequences[i][:max_length]
        return sequences
    def train(self, df_train, df_valid, feature_name, label_name):
        self.feature_name = feature_name
        self.label_name = label_name
        print(self.feature_name)
        df_train['encoded_features'] = df_train[self.feature_name].apply(lambda name: self.get_encode(name) if isinstance(name, str) else [])
        df_valid['encoded_features'] = df_valid[self.feature_name].apply(lambda name: self.get_encode(name) if isinstance(name, str) else [])
        self.trainset = df_train[['encoded_features', self.label_name]]
        self.validset = df_valid[['encoded_features', self.label_name]]
        train_sequences = df_train['encoded_features'].tolist()
        val_sequences = df_valid['encoded_features'].tolist()

        self.max_length = max(len(name) for name in train_sequences)
        train_sequences = self.padding(train_sequences, self.max_length)
        val_sequences = self.padding(val_sequences, self.max_length)

        train_labels = df_train[self.label_name].values
        val_labels = df_valid[self.label_name].values

        train_sequences = torch.LongTensor(train_sequences)
        val_sequences = torch.LongTensor(val_sequences)
        train_labels = torch.LongTensor(train_labels)
        val_labels = torch.LongTensor(val_labels)
        train_dataset = TensorDataset(train_sequences, train_labels)
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)
        val_dataset = TensorDataset(val_sequences, val_labels)
        val_loader = DataLoader(val_dataset, batch_size=self.batch_size, shuffle=False)

        self.model = TransformerModel(
            ntoken=self.vocab_size, 
            d_model=self.embedding_dim, 
            nhead=self.nhead, 
            d_hid=self.d_hid, 
            nlayers=self.nlayers, 
            dropout=self.dropout, 
            sequence_length=self.max_length)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        ratio1 =  train_labels.sum() / len(train_labels)
        ratio0 =  (len(train_labels) - train_labels.sum()) / len(train_labels)
        weight_for_class_0 = 1 / ratio0
        weight_for_class_1 = 1 / ratio1
        self.criterion = nn.CrossEntropyLoss(weight=torch.tensor([weight_for_class_0, weight_for_class_1]))
        best_loss = float('inf')
        
        for epoch in range(self.num_epochs):
            # train
            self.model.train()
            total_loss = 0.0
            for sequences, labels in train_loader:
                self.optimizer.zero_grad()
                output = self.model(sequences)
                loss = self.criterion(output, labels)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            avg_loss = total_loss / len(train_loader)
            self.train_loss_arr.append(avg_loss)
            # valid
            self.model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for val_sequences, val_labels in val_loader:
                    val_output = self.model(val_sequences)
                    val_loss += self.criterion(val_output, val_labels).item()
            avg_val_loss = val_loss / len(val_loader)
            print(f"epoch {epoch}: train loss: {avg_loss}, val loss: {avg_val_loss}.")
            self.valid_loss_arr.append(avg_val_loss)
            # early stop
            if avg_val_loss < best_loss:
                best_loss = avg_val_loss
                wait = 0
            else:
                wait += 1  # Increment patience counter
            if wait >= self.patience:
                self.stop_step = epoch
                self.best_loss = best_loss
                break
    def predict(self, X, y=None):
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        X['encoded_features'] = X[self.feature_name].apply(lambda name: self.get_encode(name) if isinstance(name, str) else [])
        x_sequences = X['encoded_features'].tolist()
        x_sequences = self.padding(x_sequences, self.max_length)
        x_labels = X[self.label_name].values
        x_sequences = torch.LongTensor(x_sequences)
        x_labels = torch.LongTensor(x_labels)
        x_dataset = TensorDataset(x_sequences, x_labels)
        x_loader = DataLoader(x_dataset, batch_size=self.batch_size, shuffle=False)
        predictions = []
        self.model.eval()
        with torch.no_grad():
            for x_sequences, x_labels in x_loader:
                x_output = self.model(x_sequences)
                x_probs = torch.softmax(x_output, dim=1)
                predictions = predictions + x_probs[:, 1].tolist()
                # labels = labels + x_labels.tolist()
        return predictions
    def log_model(self, model_uri, experiment_id=0, r_name = "run", metrics={}, registered_model_name = None):
        """
        If you need credential, make sure you have them in your environment:   

        .. code-block:: python

            os.environ['AWS_ACCESS_KEY_ID'] = os.environ.get("AWS_ACCESS_KEY_ID")
            os.environ['AWS_SECRET_ACCESS_KEY'] = os.environ.get("AWS_SECRET_ACCESS_KEY")
            os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'https://<endpoint>.<domain>.com'
            os.environ['MLFLOW_S3_BUCKET'] = 'bucketname'
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        try:
            mlflow.set_tracking_uri(model_uri)
            mlflow.set_experiment(experiment_id)
            now = datetime.datetime.now()
            with mlflow.start_run(experiment_id=experiment_id, run_name=f"{r_name}_{now}") as run:
                trainset = mlflow.data.from_pandas(self.trainset, targets=self.label_name)
                validset = mlflow.data.from_pandas(self.validset, targets=self.label_name)
                mlflow.log_input(trainset, context="trainset")
                mlflow.log_input(validset, context="validset")
                for metric_name, metric_value in metrics.items():
                    if isinstance(metric_value, (int, float)):
                        mlflow.log_metric(metric_name, metric_value)
                mlflow.log_param("vocab_size", self.vocab_size)
                mlflow.log_param("lr", self.lr)
                mlflow.log_param("embedding_dim", self.embedding_dim)
                mlflow.log_param("nhead", self.nhead)
                mlflow.log_param("d_hid", self.d_hid)
                mlflow.log_param("nlayers", self.nlayers)
                mlflow.log_param("dropout", self.dropout)
                mlflow.log_param("stop_step", self.stop_step)
                mlflow.log_param("best_loss", self.best_loss)
                mlflow.log_param("features", self.feature_name)
                if registered_model_name is None:
                    mlflow.pytorch.log_model(pytorch_model=self.model, artifact_path="Embedding")
                else:
                    mlflow.pytorch.log_model(artifact_path="Embedding", pytorch_model=self.model, registered_model_name = registered_model_name)
                mlflow.end_run()
            return True
        except Exception as e:
            raise e





#########################################
#      Classification NN model          #
#########################################
class ClassificationDataset(Dataset):
    def __init__(self, inputs, labels):
        self.inputs = inputs
        self.labels = labels

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        input_data = self.inputs[idx]
        label = self.labels[idx]
        return input_data, label


class ClassificationNNModel(nn.Module):
    def __init__(self, input_dim, min_vals = None, max_vals = None):
        """
        """
        super(ClassificationNNModel, self).__init__()
        self.min_vals = min_vals
        self.max_vals = max_vals
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)  # same as input, for loss calculation
    def forward(self, x):
        x = self.fc1(x)   # input shape is (1, N, M), N is samples number, M is feaures number
        x = torch.relu(x)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)
        x = torch.sigmoid(x)  # Apply sigmoid activation to squash output between 0 and 1
        return x


class TrainClassificationNN:
    def __init__(self, lr=0.001, num_epochs=1000, patience=10):
        self.input_dim = None
        self.lr = lr
        self.num_epochs = num_epochs
        self.patience = patience
        self.model = None
        self.optimizer = None
        self.criterion = None
        self.stop_step = 0
        self.best_loss = np.inf
        self.train_loss_arr = []
        self.valid_loss_arr = []
        self.train_min_values = None
        self.train_max_values = None
    def _normalize_data(self, X, isValid=False):
        if isValid:
            min_vals = self.train_min_values
            max_vals = self.train_max_values
        else:
            min_vals = np.min(X, axis=0)
            max_vals = np.max(X, axis=0)
            self.train_min_values = min_vals
            self.train_max_values = max_vals
        normalized_data = (X - min_vals) / (max_vals - min_vals)
        return normalized_data
    def train(self, X_train, X_valid, y_train, y_val):
        # Normalize training and validation data
        normalized_training_data = self._normalize_data(X_train)
        normalized_validation_data = self._normalize_data(X_valid, True)
        # Convert data to PyTorch tensors
        train_dataset = ClassificationDataset(torch.tensor(normalized_training_data, dtype=torch.float32), torch.tensor(y_train, dtype=torch.float32))
        valid_dataset = ClassificationDataset(torch.tensor(normalized_validation_data, dtype=torch.float32), torch.tensor(y_val, dtype=torch.float32))
        batch_size = 32
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False)
        input_dim = normalized_training_data.shape[1]
        model = ClassificationNNModel(input_dim=input_dim)

        self.input_dim = input_dim
        self.model = ClassificationNNModel(input_dim=input_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.BCELoss()
        best_loss = float('inf')
        counter = 0
        for epoch in range(self.num_epochs):
            model.train()
            running_loss = 0.0
            for batch_inputs, batch_labels in train_loader:
                self.optimizer.zero_grad()
                outputs = self.model(batch_inputs)
                loss = self.criterion(outputs, batch_labels)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item() * batch_inputs.size(0)
            epoch_loss = running_loss / len(train_loader.dataset)
            self.train_loss_arr.append(epoch_loss)
            with torch.no_grad():
                valid_loss = 0.0
                for batch_inputs, batch_labels in valid_loader:
                    outputs = self.model(batch_inputs)
                    loss = self.criterion(outputs, batch_labels)
                    valid_loss += loss.item() * batch_inputs.size(0)
                valid_loss /= len(valid_loader.dataset)
                self.valid_loss_arr.append(valid_loss)
            if valid_loss < best_loss:
                best_loss = valid_loss
                counter = 0
            else:
                counter += 1
            if counter >= self.patience:
                self.stop_step = epoch
                self.best_loss = best_loss
                break
    def predict(self, X, y_val=None):
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        with torch.no_grad():
            normalized_data = self._normalize_data(X, True)
            # valid_dataset = ClassificationDataset(torch.tensor(normalized_data, dtype=torch.float32), torch.tensor(y_val, dtype=torch.float32))
            X_tensor = torch.tensor(normalized_data, dtype=torch.float32)
            self.model.eval()
            predict_score = self.model(X_tensor)
        return predict_score.numpy()
            



#########################################
#      Classification XGB model          #
#########################################
class trainXGB:
    """Train XGB model"""
    def __init__(self, num_epochs = 1000, patience = 5, lr=0.01, subsample=0.6, colsample_bytree=0.6, reg_alpha = 1):
        self.features = []
        self.label = 'label'
        self.patience = patience
        self.num_epochs = num_epochs
        self.model_params = {
            'objective': 'binary:logistic',
            'eval_metric': 'logloss',
            'max_depth': 6,
            'learning_rate': lr,
            'subsample': subsample,
            'colsample_bytree': colsample_bytree,
            'seed': 42,
            'n_jobs': -1,
            'reg_alpha': reg_alpha, # L1 regularization
            'reg_lambda': 0 # L2
        }
        self.model = None
        self.train_loss_arr = None
        self.valid_loss_arr = None
        self.trainset = None
        self.validset = None
    def train(self, train_df, valid_df, features, label = None):
        self.features = features
        self.trainset = train_df
        self.validset = valid_df
        if label is not None:
            self.label = label
        x_train = train_df[self.features].values
        y_train = train_df[[self.label]].values
        x_val = valid_df[self.features].values
        y_val = valid_df[[self.label]].values
        dtrain = xgb.DMatrix(x_train, label=y_train, feature_names=self.features)
        dvalid = xgb.DMatrix(x_val, label=y_val, feature_names=self.features)
        # weight
        count_label_1 = np.count_nonzero(y_train)
        count_label_0 = len(y_train) - count_label_1
        scale_pos_weight = count_label_0 / count_label_1
        self.model_params['scale_pos_weight'] = scale_pos_weight
        evals_result = {}
        self.model = xgb.train(
            params=self.model_params, 
            dtrain=dtrain, 
            evals=[(dtrain, 'train'), (dvalid, 'valid')], 
            early_stopping_rounds=self.patience,
            num_boost_round=self.num_epochs,
            verbose_eval=False,
            evals_result=evals_result
        )
        self.train_loss_arr = evals_result['train']['logloss']
        self.valid_loss_arr = evals_result['valid']['logloss']
    def predict(self, X, features = None, label=None):
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        if features is not None:
            self.features = features
        if label is not None:
            self.label = label
        x_test = X[self.features].values
        y_test = X[[self.label]].values
        dtest = xgb.DMatrix(x_test, label=y_test, feature_names=self.features)
        pred_ = self.model.predict(dtest)
        return pred_
    def display_feature_importance(self):
        """display importance of xgb model"""
        fig, ax = plt.subplots()
        xgb.plot_importance(self.model, ax=ax)
        return fig
    def log_model(self, model_uri, experiment_id=0, r_name = "run", metrics={}, registered_model_name = None):
        """
        If you need credential, make sure you have them in your environment:   

        .. code-block:: python

            os.environ['AWS_ACCESS_KEY_ID'] = os.environ.get("AWS_ACCESS_KEY_ID")
            os.environ['AWS_SECRET_ACCESS_KEY'] = os.environ.get("AWS_SECRET_ACCESS_KEY")
            os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'https://<endpoint>.<domain>.com'
            os.environ['MLFLOW_S3_BUCKET'] = 'bucketname'
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        try:
            mlflow.set_tracking_uri(model_uri)
            mlflow.set_experiment(experiment_id)
            now = datetime.datetime.now()
            with mlflow.start_run(experiment_id=experiment_id, run_name=f"{r_name}_{now}") as run:
                trainset = mlflow.data.from_pandas(self.trainset[self.features + [self.label]], targets=self.label)
                validset = mlflow.data.from_pandas(self.validset[self.features + [self.label]], targets=self.label)
                mlflow.log_input(trainset, context="trainset")
                mlflow.log_input(validset, context="validset")
                for metric_name, metric_value in metrics.items():
                    if isinstance(metric_value, (int, float)):
                        mlflow.log_metric(metric_name, metric_value)
                for param_name, param_value in self.model_params.items():
                    mlflow.log_param(param_name, param_value)
                if registered_model_name is None:
                    mlflow.xgboost.log_model(xgb_model=self.model, artifact_path='xgb')
                else:
                    mlflow.xgboost.log_model(
                        xgb_model=self.model, 
                        artifact_path='xgb',
                        registered_model_name=registered_model_name)
                mlflow.end_run()
            return True
        except Exception as e:
            raise e


#########################################
#          K-Means Cluster              #
#########################################
class KMeansModel:
    """
    KMeansModel

    The `KMeansModel` class is a Python implementation of the K-means clustering algorithm. Clustering is a type of unsupervised machine learning that partitions data into groups (clusters) based on similarity. The K-means algorithm aims to divide the data into K clusters, where each cluster is represented by its centroid.

    To use the `KMeansModel` class, follow these steps:

    1. Create an instance of the class with an optional parameter `K` (number of clusters, default is 3).

    .. code-block:: python

        from quick_anomaly_detector.models import KMeansModel

        kmeans = KMeansModel(K=3)

    2. Train the model on your data using the `train` method.

    .. code-block:: python

        centroids, labels = kmeans.train(X, max_iters=10)

    - `X`: Input data matrix.
    - `max_iters`: Maximum number of iterations for the K-means algorithm (default is 10).

    3. Access the resulting centroids and labels.

    .. code-block:: python

        centroids = kmeans.centroids
        labels = kmeans.labels

    4. Optionally, perform image compression using the `image_compression` method.

    .. code-block:: python

        compressed_img = kmeans.image_compression(image_path, color_K=16, max_iters=10)

    """

    def __init__(self, K=3):
        """
        Initialize a KMeansModel instance.

        Parameters:
            K (int): Number of centroids (clusters). Default is 3.
        """
        self.K = K

    def kMeans_init_centroids(self, X, K):
        """
        Randomly initialize centroids.

        Parameters:
            X (ndarray): Input data matrix.
            K (int): Number of centroids.

        Returns:
            ndarray: Initialized centroids.
        """
        randidx = np.random.permutation(X.shape[0])
        centroids = X[randidx[:K]]
        return centroids

    def find_closest_centroids(self, X, centroids):
        """
        Find the closest centroid for each example.

        Parameters:
            X (ndarray): Input data matrix.
            centroids (ndarray): Current centroids.

        Returns:
            ndarray: Index of the closest centroid for each example.
        """
        K = centroids.shape[0]
        idx = np.zeros(X.shape[0], dtype=int)
        for i in range(X.shape[0]):
            distances = np.linalg.norm(X[i] - centroids, axis=1)
            idx[i] = np.argmin(distances)
        return idx

    def compute_centroids(self, X, idx, K):
        """
        Compute new centroids based on assigned examples.

        Parameters:
            X (ndarray): Input data matrix.
            idx (ndarray): Index of the closest centroid for each example.
            K (int): Number of centroids.

        Returns:
            ndarray: New centroids.
        """
        m, n = X.shape
        centroids = np.zeros((K, n))
        for k in range(K):
            indices = (idx == k)
            centroids[k, :] = np.mean(X[indices, :], axis=0)
        return centroids

    def train(self, X, K=3, max_iters=10):
        """
        Train the KMeansModel.

        Parameters:
            X (ndarray): Input data matrix.
            K (int): Number of centroids (clusters). Default is 3.
            max_iters (int): Maximum number of iterations. Default is 10.

        Returns:
            tuple: Resulting centroids and index of each data point's assigned cluster.
        """
        initial_centroids = self.kMeans_init_centroids(X, K)
        m, n = X.shape
        K = initial_centroids.shape[0]
        centroids = initial_centroids
        previous_centroids = centroids  
        idx = np.zeros(m)  
        for i in range(max_iters):
            idx = self.find_closest_centroids(X, centroids)
            centroids = self.compute_centroids(X, idx, K)
        return centroids, idx
    
    def image_compression(self, image_path, color_K=16, max_iters=10):
        """
        Perform image compression using K-means clustering.

        Parameters:
            image_path (str): Path to the input image file.
            color_K (int): Number of colors for compression. Default is 16.
            max_iters (int): Maximum number of iterations for K-means. Default is 10.

        Returns:
            ndarray: Compressed image.
        """
        original_img = plt.imread(image_path)
        X_img = np.reshape(original_img, (original_img.shape[0] * original_img.shape[1], 4))
        centroids, idx = self.train(X_img, color_K, max_iters)
        X_recovered = centroids[idx, :]
        X_recovered = np.reshape(X_recovered, original_img.shape)
        return X_recovered



#####################################
#      Lower the string             #
#####################################
class convertStr(BaseEstimator):
    """
    convertStr class is designed to convert specific columns in a DataFrame to string type. 
    """
    def __init__(self, features=[]):
        self.features = features
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_ = X.copy()
        for col in self.features:
            X_[col] = X_[col].astype(str)
        return X_  



#########################################################
#         Customeized Imputer Class                     #
#########################################################
class ImputerNa(BaseEstimator, TransformerMixin):
    """
    A custom imputer transformer that extends scikit-learn's SimpleImputer
    while preserving column names after imputation.

    Parameters
    strategy : {'mean', 'median', 'most_frequent', 'constant'}, default='mean'   
        The imputation strategy.   
    fill_value : str, int, or float, optional    
        The constant value to fill missing values when strategy='constant'.

    Attributes
    strategy : str   
        The imputation strategy.
    fill_value : str, int, or float   
        The constant value to fill missing values when strategy='constant'.

    Methods
    fit(X, y=None)   
        Fit the imputer to the data.
    transform(X, y=None)   
        Transform the data by imputing missing values and preserving column names.

    Examples

        .. code-block:: python
    
        from sklearn.pipeline import Pipeline
        quick_anomaly_detector.data_process import CustomImputer

        fill_values = {
            'column1': 0,
            'column2': ''
        }
        pipeline = Pipeline([
            ('imputer', CustomImputer(strategy='mean')),
            ('fillna', CustomImputer(strategy='constant', fill_value=fill_values)),
        ])
        X_train_imputed = pipeline.fit_transform(X_train)

    """
    def __init__(self, strategy='mean', fill_values=None):
        self.strategy = strategy
        self.fill_values = fill_values

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_filled = X.copy()
        X_filled = X_filled.fillna(self.fill_values)
        return X_filled


#####################################
#      Select Features + Label      #
#####################################
class SelectFeatures(BaseEstimator):
    """
    This class is for pipeline using of select features and label
    """
    def __init__(self, features=[], label='label'):
        self.features = features
        self.label = [label]
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_ = X.copy()
        return X_[self.features+self.label]


#####################################
#      Lower the string             #
#####################################
class LowerStr(BaseEstimator):
    """
    This class is for pipeline using of make the string value to lower letter.
    """
    def __init__(self, features=[]):
        self.features = features
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_ = X.copy()
        for col in self.features:
            X_[col] = X_[col].str.lower()
        return X_  


#####################################
#      Length of the string         #
#####################################
class LengthStr(BaseEstimator):
    """
    This class is for pipeline using of make the string value to lower letter.
    """
    def __init__(self, features=[]):
        self.features = features
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_ = X.copy()
        for col in self.features:
            X_[f"{col}_len"] = X_[col].str.len()
        return X_



#####################################
#      Log value of columns         #
#####################################
class LogTransform(BaseEstimator):
    """
    This class is for pipeline using of calculate log.
    """
    def __init__(self, features=[]):
        self.features = features
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_ = X.copy()
        for col in self.features:
            X_[f"log_{col}"] = X_[col].apply(lambda x: np.log(x+0.001))
            X_[f"square05_{col}"] = X_[col].apply(lambda x: x ** 0.5)
        return X_ 


#####################################
#      Set Numeric DataType         #
#####################################
class NumericDataType(BaseEstimator):
    """
    This class is for set data into numberic datatype.
    """
    def __init__(self, features=[]):
        self.features = features
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_ = X.copy()
        for col in self.features:
            X_[col] = X_[col].apply(pd.to_numeric, errors='coerce')
        return X_


#####################################
#      Calculate Similarity         #
#####################################
class Similarity(BaseEstimator):
    """
    This class is for calculate similarity of 2 string.
    """
    def __init__(self, pairs=[]):
        self.pairs = pairs
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_ = X.copy()
        for pair in self.pairs:
            X_[f'{pair[0]}_{pair[1]}_score'] = self.get_similarity(X_, pair[0], pair[1])
        return X_
    def get_similarity(self, df, column_str_1, column_str_2):
        if df.empty:
            raise ValueError("DataFrame is empty.")
        if column_str_1 not in df.columns or column_str_2 not in df.columns:
            raise ValueError("One or more specified columns not found in the DataFrame.")
        def jaccard_similarity(str1, str2):
            if not str1 or not str2:
                return 0.0
            a = set(str1)
            b = set(str2)
            c = a.intersection(b)
            return float(len(c)) / (len(a) + len(b) - len(c))
        df.loc[:, 'similarity_score'] = df.apply(lambda row: jaccard_similarity(row[column_str_1], row[column_str_2]), axis=1)
        return df['similarity_score'].values



#####################################
#            Label Encode           #
#####################################
class LabelEncode(BaseEstimator):
    def __init__(self, features):
        self.features = features
        self.label_encoder = LabelEncoder()
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_ = X.copy()
        for col in self.features:
            self.label_encoder.fit(X_[col])
            X_[f'{col}_encode'] = self.label_encoder.transform(X_[col])
        return X_


#####################################
#            Padding                #
#####################################
class Padding(BaseEstimator, TransformerMixin):
    """This class is for data pipeline that padding for str columns"""
    def __init__(self, features, max_lengths=None):
        self.features = features
        self.max_lengths = max_lengths
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_ = X.copy()
        for col, max_length in self.max_lengths.items():
            X_[col] = X_[col].str.pad(width=max_length, side='right', fillchar='-')
        return X_
    def fit_transform(self, X, y=None):
        X_ = X.copy()
        self.max_lengths = {}
        for col in self.features:
            max_length = X_[col].str.len().max()
            self.max_lengths[col] = max_length
            X_[col] = X_[col].str.pad(width=max_length, side='right', fillchar='-')
        return X_



#####################################
#    Log Model to ML Flow           #
#####################################