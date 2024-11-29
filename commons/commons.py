import pickle
import numpy as np
import pandas as pd
from configparser import ConfigParser
import os
ROOT_DIR =  os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.ini')

print(CONFIG_PATH)

config = ConfigParser()
config.read(CONFIG_PATH)



class CommonManager:
    """
    A class to manage and dynamically access Config Cathegories

    Attributes:

    """

    def __init__(self):
        """
        Initializes the DatasetPaths class with the base commons.

        Args:

        """
        self.ROOT =os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
        self.DB_PATH = config.get("PATHS", f"DB_PATH")
        self.MODEL_PATH = config.get("PATHS", "MODEL_PATH")
    @staticmethod
    def preprocess_data(X):
        print(f"Preprocessing data")
        return X
    @staticmethod
    def persist_model(model, path):
        print(f"Persisting the model to {path}")
        model_dir = os.path.dirname(path)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        with open(path, "wb") as file:
            pickle.dump(model, file)
        print(f"Done")

    @staticmethod
    def load_model(path):
        print(f"Loading the model from {path}")
        with open(path, "rb") as file:
            model = pickle.load(file)
        print(f"Done")
        return model

if __name__ == "__main__":
    common = CommonManager()
    print(common.DATA)
