"""
This function can be used to convert the string being read to int or list form
For example
When reading the location data from one of the csv files
I got an error in which accessing the x value of the location
by df['location'][0] gave me '[' meaning that the values were
being read as a string therefore this function can convert it
back to normal list of coordinates

Usage:
from remove_string import convert_to_int
shot['location'] = convert_to_int(shot['location'])
"""
from ast import literal_eval
import numpy as np

def convert_to_int(df):
    for i in np.arange(len(df)):
        df[i] = literal_eval(df[i])
    return df