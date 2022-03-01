import pandas as pd
import datetime

dbpath = "data/database.csv"

def save(*args):
    idx = len(pd.read_csv(dbpath))
    new_df = pd.DataFrame(args,
                         index = [idx])
    new_df.to_csv(dbpath,mode = "a", header = False)
    return None

def load_list():
    info_list = []
    df = pd.read_csv(dbpath)
    for i in range(len(df)):
        info_list.append(df.iloc[i].tolist())
    return info_list

def now_index():
    df = pd.read_csv(dbpath)
    return len(df)-1


def load_data(idx):
    df = pd.read_csv(dbpath)
    info_data = df.iloc[idx]
    return info_data


if __name__ =="__main__":
    load_list()