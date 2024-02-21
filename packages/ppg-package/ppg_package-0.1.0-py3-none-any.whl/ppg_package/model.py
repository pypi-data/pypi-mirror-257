import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset
import os

class CustomDataset(Dataset):
    def __init__(self, data_directory, columns_of_interest):
        self.data = []
        self.min_max_values = {}  # 用于存储每列的最小和最大值

        for data_file in os.listdir(data_directory):
            if data_file.endswith(".xlsx"):
                data_path = os.path.join(data_directory, data_file)
                df = pd.read_excel(data_path, usecols=columns_of_interest)
                df_normalized = self.normalize_dataframe(df)
                for _, row in df_normalized.iterrows():
                    numeric_data = row.drop('CO').astype(float)
                    co_label = row['CO'].astype(float)
                    self.data.append((numeric_data, co_label))

    def normalize_dataframe(self, df):
        for column in df.columns:
            min_value = df[column].min()
            max_value = df[column].max()
            self.min_max_values[column] = (min_value, max_value)
            df[column] = (df[column] - min_value) / (max_value - min_value)
        return df

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        numeric_data, co_label = self.data[idx]
        return torch.tensor(numeric_data.values, dtype=torch.float32), torch.tensor(co_label, dtype=torch.float32).unsqueeze(0)


class NumericNetwork(nn.Module):
    def __init__(self, numeric_features):
        super(NumericNetwork, self).__init__()
        self.layer1 = nn.Sequential(nn.Linear(numeric_features, 64), nn.BatchNorm1d(64), nn.ReLU())
        self.layer2 = nn.Sequential(nn.Linear(64, 32), nn.BatchNorm1d(32), nn.ReLU())
        self.layer3 = nn.Sequential(nn.Linear(32, 16), nn.BatchNorm1d(16), nn.ReLU())
        self.output = nn.Linear(16, 1)
        self._initialize_weights()

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.output(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
