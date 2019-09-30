import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def fileUpload(filePath): #takes in the file path and returns it as a pandas csv variable
    data = pd.read_csv(filePath)
    return data


def fileOutput(dataFrame): #takes in the dataframe and writes to a csv file
    dataFrame.to_csv('lulw.csv', index=None, header=True)
    #return "Successfully exported %s.csv" %fName