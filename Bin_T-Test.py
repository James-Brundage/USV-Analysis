'''
Takes the Updated Binned tab from the mastersheet and runs a t-test for each time bin with the No stim group.
P-values are unadjusted. Finally the p-values are plotted against time bin to demonstrate where significance
is achieved.

File is located on box, but exact path name should still be updated.
'''

import pandas as pd
import os
import xlrd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

# Reads in correct sheet from file.
path = '/Users/jamesbrundage/Box/USV MStim/MStim Withdrawal USV Mastersheet UPDATED 11620.xlsx'

# Reads in correct sheet from excel file
df = pd.read_excel(path, sheet_name='Updated Binned')

# Creates the hour column to locate time
df['Hour'] = df['Time Bin'] / 3600

# Narrow dataset to only desired time point range
rng = [1.5, 2]

# Filters the between 1.5 hours and 2 hours
df = df[(df['Hour'] >= 1.5) & (df['Hour'] <= 2)]

# Fixes the weird group labeled incorrectly
def fixer (freq):
    if freq == 'No stim':
        return 'No Stim'
    else :
        return freq
df['Vibration Frequency'] = df['Vibration Frequency'].apply(fixer)

# Gets unique set of bins and vibration frequencies
bins = list(set(df['Time Bin']))
freqs = list(set(df['Vibration Frequency']))

# Creates t-test ready dataframe
dffs_lst = []
for b in bins:

    dfs_lst = []
    for f in freqs:
        df_w = df[(df['Time Bin'] == b) & (df['Vibration Frequency'] == f)].copy()
        rew = df_w.groupby('Rat Number').mean()['Rewarding Calls']

        obj = pd.DataFrame()
        obj['Rewarding Calls ' + f] = rew

        dfs_lst.append(obj)


    dff = pd.concat(dfs_lst, axis=1)
    dff['Time Bin'] = b

    dffs_lst.append(dff)
dff_f = pd.concat(dffs_lst)
dff_f.sort_values('Time Bin', inplace=True)

# Gets list of unique vals for next section
freqs = ['45Hz', '80Hz', '115Hz']
bins = list(set(dff_f['Time Bin']))

# Creates p-value df, so these can be visualized for each bin
vals_lst = []
for f in freqs:

    pval = []
    bin = []
    for b in bins:
        df_w = dff_f[dff_f['Time Bin'] == b]
        tt = ttest_ind(df_w['Rewarding Calls No Stim'], df_w['Rewarding Calls ' + f], equal_var=False)
        pval.append(tt[1])
        bin.append(b)

    pvals_df = pd.DataFrame()
    pvals_df['Time Bin'] = bin
    pvals_df['p-values'] = pval
    pvals_df['Vibration Frequency'] = f
    pvals_df.sort_values('Time Bin', inplace=True)
    vals_lst.append(pvals_df)
final_df = pd.concat(vals_lst)
final_df = final_df.fillna(1)

# Plots the p-values for each frequency by time bin.
for f in freqs:
    df = final_df[final_df['Vibration Frequency'] == f]
    plt.plot(df['Time Bin'], df['p-values'])

plt.axhline(0.05, color='r')
plt.title('P-value by Bins')
plt.ylabel('p-value')
plt.xlabel('Time Bin')
plt.legend(freqs)
plt.show()









