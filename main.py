import wx
import eel
import numpy as np
import pandas as pd
from functions import preprocessing, get_vectorize, return_match_pair, awesome_cossim_top

#Global Files
FILE1 = None
FILE2 = None

eel.init('web')

@eel.expose
def get_file_1(wildcard=".csv;.xlsx"):
    global FILE1
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
        if path.endswith(".csv"):
            FILE1 = pd.read_csv(path)
        else:
            FILE1 = pd.read_excel(path)
        header = [path]
        for i in FILE1.columns:
            FILE1.rename(columns={i:i+"_F1"}, inplace=True)
            header.append(i+"_F1")
        return header
    else:
        path = None
    dialog.Destroy()


@eel.expose
def get_file_2(wildcard=".csv;.xlsx"):
    global FILE2
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
        if path.endswith(".csv"):
            FILE2 = pd.read_csv(path)
        else:
            FILE2 = pd.read_excel(path)
        header = [path]
        for i in FILE2.columns:
            FILE2.rename(columns={i:i+"_F2"}, inplace=True)
            header.append(i+"_F2")
        return header
    else:
        path = None
    dialog.Destroy()


@eel.expose
def perform_fuzzy(col1, col2, range):
    FILE1['INDEX'] = FILE1.index
    FILE1.insert(0, 'INDEX',  FILE1.pop('INDEX'))
    FILE1.fillna({col1:''}, inplace=True)

    A = FILE1[col1].tolist()
    B = FILE2[col2].tolist()
    A_C = preprocessing(FILE1, col1, col1+'_CLEAN')
    B_C = preprocessing(FILE2, col2, col2+'_CLEAN')
    cca_lookup, client_table_array = get_vectorize(A, B)

    #Perform Fuzzy
    matches = awesome_cossim_top(cca_lookup, client_table_array.transpose(), 1000, float(int(range)/100))
    matches_df = return_match_pair(matches, A+B, B, len(A), col1, col2)

    #Save it
    app = wx.App(None)
    style = wx.FD_SAVE
    dialog = wx.FileDialog(None, 'Open', style=style)
    if dialog.ShowModal() == wx.ID_OK:
        save_path = dialog.GetPath()
        matches_df.to_excel(save_path+".xlsx", index=False)
    dialog.Destroy()

    return 1

eel.start("index.html", size=(1200,800))