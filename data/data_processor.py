import sqlite3
import pandas as pd

class DataProcesor:
    def __init__(self):
        """
        Init method

        """
    def df_to_sql(self, df,path):
        con = sqlite3.connect(path)

        df.to_sql("train", con, if_exists="replace")
        #con.execute(f"vacuum main into '{path}' ")
        con.execute("VACUUM")
        db_location = con.execute("PRAGMA database_list").fetchall()[0][2]

        print(db_location)
        return db_location





if __name__ == "__main__":
    data = DataProcesor()
