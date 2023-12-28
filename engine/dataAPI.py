import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Ai import Movie

def GetAllMovies(checkAdult):
    raw = pd.read_csv("engine\\new_data.csv", delimiter=',', encoding='utf-8', low_memory=False)
    
    if checkAdult:
        movieListAll = []
        
        rowNumber = raw.shape[0]
        for i in range(22):
            createMovie = Movie(raw.iloc[i][0],raw.iloc[i][2],raw.iloc[i][3],raw.iloc[i][4],raw.iloc[i][5],raw.iloc[i][6],raw.iloc[i][7])
            movieListAll.append(createMovie)
        return movieListAll
    
    else:
        movieList = []
        raw = raw[raw['isAdult'] == 0]
        rowNumber = raw.shape[0]

        for i in range(rowNumber):
            createMovie = Movie(raw.iloc[i][0],raw.iloc[i][2],raw.iloc[i][3],raw.iloc[i][4],raw.iloc[i][5],raw.iloc[i][6],raw.iloc[i][7])
            movieList.append(createMovie)
        return movieList