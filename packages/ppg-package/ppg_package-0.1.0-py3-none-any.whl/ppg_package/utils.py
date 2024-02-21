import torch
import pandas as pd
from .model import CustomDataset, NumericNetwork


def load_model(model_path, input_features):
    model = NumericNetwork(numeric_features=input_features)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model


def prepare_data_loader(data_directory, columns_of_interest, batch_size=1):
    dataset = CustomDataset(data_directory, columns_of_interest)
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False)
    return data_loader


def unnormalize(value, min_value, max_value):
    return value * (max_value - min_value) + min_value

def predict(model, data_loader, min_max_values):
    predictions = []
    with torch.no_grad():
        for data, co_label in data_loader:
            output = model(data)
            predicted_co = unnormalize(output.numpy(), min_max_values['CO'][0], min_max_values['CO'][1])
            predictions.append(predicted_co)
    return predictions
    

def read_and_predict(data_directory, model_path, columns_of_interest):
    model = load_model(model_path, len(columns_of_interest) - 1)
    dataset = CustomDataset(data_directory, columns_of_interest)
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False)
    predictions = predict(model, data_loader, dataset.min_max_values)
    return predictions

def predict_with_preloaded_data(model, data_tensor):
    predictions = []
    with torch.no_grad():
        output = model(data_tensor)
        predictions.append(output)
    return predictions

def read_and_predict_with_tensor(data_tensor, model_path, columns_of_interest):
    # 加载模型
    model = NumericNetwork(numeric_features=len(columns_of_interest)-1)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # 预测
    predictions = predict_with_preloaded_data(model, data_tensor)
    return predictions

