import pandas as pd
import os
from src.mlProject.logging import logger
import pickle
from src.mlProject.entity.config_entity import ModelPredictionConfig


class ModelPrediction:
    def __init__(self, config: ModelPredictionConfig):
        self.config = config

    
    def recommend(self, movie: str):
        with open(self.config.movie_model_path, 'rb') as movie_file:
            movie_df = pickle.load(movie_file)
        with open(self.config.similarity_model_path, 'rb') as similarity_file:
            similarity = pickle.load(similarity_file)
        index = movie_df[movie_df['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
        for i in distances[1:6]:
            print(movie_df.iloc[i[0]].title) 