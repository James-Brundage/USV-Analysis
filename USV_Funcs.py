import numpy as np
import pandas as pd
import seaborn as sns
import os, sys

'''This describes what happens here'''

# Stitches the separate excel files together, creates columns for which file they came from, creates and adjusted time column
# returns a dataframe of the whole experiment.
def USV_stitch(folder_path):
    # Creates lists of path names, df from each one
    paths_lst = os.listdir(folder_path)
    dfs_lst = []
    for name in paths_lst[:]:
        df = pd.read_excel(folder_path + '\\' + name)
        dfs_lst.append(df)
    # Creates dictionary from df and filename
    dictt = dict(zip(paths_lst, dfs_lst))

    # Creates Adjusted time and Parts columns
    for k in dictt:
        if k.find('art_1') > -1:
            df = dictt[k]
            lista = []
            for i in range(0, len(df['ID'])):
                lista.append('Part 1')
            df['Parts'] = lista

        elif k.find('art_2') > -1:
            df = dictt[k]
            listb = []
            for i in range(0, len(df['ID'])):
                listb.append('Part 2')
            df['Parts'] = listb

        else:
            df = dictt[k]
            listc = []
            for i in range(0, len(df['ID'])):
                listc.append('art 3')
            df['Parts'] = listc
    for k in dictt:
        df = dictt[k]
        lista
        if df['Parts'][0] == 'art 1':
            df['Adjusted Time'] = df['Begin Time (s)']

        elif df['Parts'][0] == 'art 2':
            df['Adjusted Time'] = df['Begin Time (s)'] + (60 * 45)

        else:
            df['Adjusted Time'] = df['Begin Time (s)'] + (60 * 45) + (60 * 60)
    dict_output = [dictt[paths_lst[0]], dictt[paths_lst[1]], dictt[paths_lst[2]]]

    # Concatenates to single df
    dff = pd.concat(dict_output)

    dff['Rewarding/Aversive'] = dff['Principal Frequency (kHz)'].apply(lambda x: 'Rewarding' if x > 25 else 'Aversive')
    return dff

# Bins df into two min bins, returns Original Df with Bins columns, as well as a binned df with Columns: Time Bin, Total Call
# Rewarding Calls, Aversive Calls
def Binner(df):
    hist_arr = np.histogram(df['Adjusted Time'],range=(0,10800),bins=90)

    # Creates unbinned call time bins columns and adds to df
    unbinned_time_col_lst = []
    for time in df['Adjusted Time']:

        for bin in hist_arr[1]:

            if time < bin:
                unbinned_time_col_lst.append(bin)
                break
    df['Time Bin'] = unbinned_time_col_lst

    Tot_Call_Bin = df.groupby(['Time Bin']).count()['ID']
    Rew_Call_Bin = df[df['Rewarding/Aversive'] == 'Rewarding'].groupby(['Time Bin']).count()['ID']
    Aver_Call_Bin = df[df['Rewarding/Aversive'] == 'Aversive'].groupby(['Time Bin']).count()['ID']
    Av_Freq_Bin = df.groupby(['Time Bin']).mean()['Principal Frequency (kHz)'].fillna(0)
    # Creates binned rew call columns for binned Df
    Binned_Rew_Call = []
    for bin in hist_arr[1][1:]:
        dfr = df[df['Rewarding/Aversive']=='Rewarding']
        num = dfr[dfr['Time Bin']==bin].count()['ID']

        if num > 0:
            Binned_Rew_Call.append(num)

        else:
            Binned_Rew_Call.append(0)
    # Creates binned av column for Binned Df
    Binned_Av_Call = []
    for bin in hist_arr[1][1:]:
        dfr = df[df['Rewarding/Aversive'] == 'Aversive']
        num = dfr[dfr['Time Bin'] == bin].count()['ID']

        if num > 0:
            Binned_Av_Call.append(num)

        else:
            Binned_Av_Call.append(0)
    # Creates principal Frequency col
    Binned_Principal_Freq = []
    for bin in hist_arr[1][1:]:
        dfr = df
        num = dfr[dfr['Time Bin'] == bin].mean()

        # print(num['Principal Frequency (kHz)'])

        if num['Principal Frequency (kHz)'] > 0:
            Binned_Principal_Freq.append(num['Principal Frequency (kHz)'])

        else:
            Binned_Principal_Freq.append(0)


    # Creates binned Df
    BinnedDF = pd.DataFrame()
    BinnedDF['Time Bin'] = hist_arr[1][1:]
    BinnedDF['Rewarding Calls'] = Binned_Rew_Call
    BinnedDF['Aversive Calls'] = Binned_Av_Call
    BinnedDF['Total Calls'] = BinnedDF['Rewarding Calls'] + BinnedDF['Aversive Calls']
    BinnedDF['Average Principal Frequency'] = Binned_Principal_Freq


    return [df,BinnedDF]

def Categorical_Adder(df_lst):
    Rat_Number = input('What is the Rat Number? ')
    Technician = input('Who was the technician for this experiment? ')
    Vib_Freq = input('What was the vibration frequency? ')
    ret_df_lst = []
    for df in df_lst:
        df['Rat Number'] = [Rat_Number] * len(df)
        df['Technician'] = [Technician] * len(df)
        df['Vibration Frequency'] = [Vib_Freq] * len(df)

        Time_Category_lst = []
        for time in df['Time Bin']:

            if time < 1800:
                Time_Category_lst.append('Baseline')

            elif time < 2700:
                Time_Category_lst.append('Stim')

            else:
                Time_Category_lst.append('Recording')

        df['Time Category'] = Time_Category_lst

        ret_df_lst.append(df)

    return ret_df_lst


    
    
    


path = r"R:\SteffensenLab\FREELY-MOVING ANIMAL STUDIES--DO NOT DELETE\MStim\MStim + USVs Nov 2019\MStim + USVs Exported Excel Files\45Hz\Cage 1\Stripe 1"










