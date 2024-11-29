
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os
from commons.commons import CommonManager as CM
from data.data_processor import DataProcesor
class ModelManager:
    """
    A class to manage and dynamically access Config Cathegories

    Attributes:

    """

    def __init__(self):
        """
        Initializes the DatasetPaths class with the base commons.

        Args:

        """
        self.root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

    def load_train_data(self,path):

        print(f"Reading train data from the database: {path}")
        con = sqlite3.connect(path)
        data_train = pd.read_sql('SELECT * FROM train', con)
        print(data_train)
        con.close()
        X = data_train.drop(columns=['trip_duration'])
        y = data_train['trip_duration']
        return X, y

    def fit_model(self, X, y):
        print(f"Fitting a model")
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        score = mean_squared_error(y, y_pred)
        print(f"Score on train data {score:.2f}")
        return model


    def PrepareData(self, data, del_columns: list, isTimeProceable: bool, tp_colums: list):

        if del_columns != []:
            for colum in del_columns:
                data = data.drop(columns=[colum])
        if isTimeProceable:
            for colum in tp_colums:

                data[colum] = pd.to_datetime(data[colum], errors='coerce')
                errores = data[data[colum].isna()]
                if not errores.empty:
                    print("Filas con valores inválidos en la columna:")
                    print(errores)

                data[colum] = pd.to_datetime(data[colum])
                data[colum] = data[colum].apply(lambda x: x.timestamp())
                data = data.drop(columns=[colum])
        data = data.drop(columns=["store_and_fwd_flag"])
        return data

if __name__ == "__main__":

    commons = CM()
    train = ModelManager()
    data = pd.read_csv(f"{commons.ROOT}{commons.DB_PATH}", compression="zip")

    delc=["id", "dropoff_datetime"]
    time= ["pickup_datetime"]

    db = train.PrepareData(data, delc, True, tp_colums=time)

    data = DataProcesor()
    data_path= f"{commons.ROOT}\\data\\train.db"
    path = data.df_to_sql(db,data_path)
    model_manager = ModelManager()

    X_train, y_train = model_manager.load_train_data(path)
    CM.preprocess_data(X=X_train)
    model = model_manager.fit_model(X_train, y_train)
    CM.persist_model(model, f"{commons.ROOT}{commons.MODEL_PATH}")
