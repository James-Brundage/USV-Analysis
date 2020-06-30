import numpy as np
import pandas as pd
import seaborn as sns
import os, sys
from USV_Funcs import USV_stitch, Binner, Categorical_Adder

path = '/Users/jamesbrundage/Box/USV MStim/Excel Files (May 2020)'

def file_pths_df (pth):
    '''
    :param pth: The general path to the files being analyzed. In this instance, the path is listed above for example.
    :return: Dataframe with the columns Path, Animal Name and Frequency which denote the paths to be used by the stitcher.
    '''
    an_files = []
    for root, dirs, files in os.walk(path):
        if root[len(path):].count(os.sep) < 1:
            for name in dirs:
                an_files.append(os.path.join(root,name))

    lst = []
    for f in an_files:
        for root, dirs, files in os.walk(f):
            for name in dirs:
                lst.append(os.path.join(root, name))

    df = pd.DataFrame()
    df['Path'] = lst

    def animals (path):

        lst = ['Stripe 1','Stripe 2','Stripe 3']
        for a in lst:
            if path.find(a) > -1:
                return a + ' May'

    def freq (path):
        lst = ['45Hz', '80Hz', '115Hz', 'No Stim']
        for f in lst:
            if path.find(f) > -1:
                return f

    df['Animal Name'] = df['Path'].apply(animals)
    df['Frequency'] = df['Path'].apply(freq)

    return df

pths_df = file_pths_df(path)

dfs_lst = []
for index, row in pths_df.iterrows():

    dff = USV_stitch(row['Path'])
    dfs = Binner(dff)
    dfs = Categorical_Adder(dfs, inpt=False, rn=row['Animal Name'], tc='PB', f=row['Frequency'])

    dfs_lst.append(dfs[1])

dff = pd.concat(dfs_lst)

pd.DataFrame.to_clipboard(dff)















