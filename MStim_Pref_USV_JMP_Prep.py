import pandas as pd
import matplotlib.pyplot as plt

path = '/Users/jamesbrundage/Box/USV MStim/MStim Withdrawal USV Mastersheet UPDATED 11620.xlsx'

# Reads in correc tsheet fro mexcel file
df = pd.read_excel(path, sheet_name='Updated Binned')

# Creates the hour column to locate time
df['Hour'] = df['Time Bin'] / 3600

# Narrow dataset to only desired time point range
rng = [1.5, 2]

# Filters the between 1.5 hours and 2 hours
df = df[(df['Hour'] >= 1.5) & (df['Hour'] <= 2)]








