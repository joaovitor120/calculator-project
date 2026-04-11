import csv
import pandas as pd
import os

user_csv_path = "./csv_exported/User_data.csv"
calc_csv_path = "./csv_exported/Calc_datas.csv"

def to_csv(dict, path):
    if os.path.isfile(path):
        os.remove(path)
        df_user = pd.DataFrame((dict))
        df_user.to_csv(path)
    else:
        df_user = pd.DataFrame((dict))
        df_user.to_csv(path)






