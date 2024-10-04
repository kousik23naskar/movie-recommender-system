import pandas as pd
import os
from src.mlProject.logging import logger
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from src.mlProject.entity.config_entity import ModelTrainerConfig



class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    
    def build_movie_recommendation_model(self):
        movie_df = pd.read_csv(self.config.train_data_path)
        cv = CountVectorizer(max_features=self.config.max_features,stop_words='english')

        vector = cv.fit_transform(movie_df['tags']).toarray()
        similarity = cosine_similarity(vector)
        #print(similarity.shape)
        #print(movie_df[movie_df['title'] == 'The Lego Movie'].index[0])

        movie_pkl_file_path = os.path.join(self.config.root_dir, self.config.movie_model)
        similarity_pkl_file_path = os.path.join(self.config.root_dir, self.config.similarity_model)
        #print(f"pkl file path:\n{movie_pkl_file_path}\n{similarity_pkl_file_path}\n")

        pickle.dump(movie_df,open(movie_pkl_file_path,'wb'))
        pickle.dump(similarity,open(similarity_pkl_file_path,'wb'))
