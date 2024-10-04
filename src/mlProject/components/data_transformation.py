import os
import pandas as pd
from src.mlProject.utils.common import convert, convert_cast, fetch_director, remove_space, perform_stem
from src.mlProject.logging import logger
from src.mlProject.entity.config_entity import DataTransformationConfig



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config


    ##Note:One can perform all kinds of EDA, different data transformation techniques such as Scaler,
    ##PCA and all in ML cycle here before passing this data to the model      


    def perform_data_transformation(self):
        try:
            movies = pd.read_csv(self.config.data_path1)
            credits = pd.read_csv(self.config.data_path2)

            print(f"Shape of movie data before merge: {movies.shape}")
            print(f"Shape of movie data before merge: {credits.shape}\n")

            movies = movies.merge(credits,on='title')
            #print("Table after merging movies and credits dataset \n")
            #print(movies.head(2))
            print(f"Shape of movie data after merge of movies and credits dataframe: {movies.shape}\n")

            # Keeping important columns for recommendation
            movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
            #print("Checking selected columns in following table \n")
            #print(movies.head(2))

            ##Checking and dropping null values and duplicate columns
            print(f"=========checking null values===========\n{movies.isnull().sum()}\n")
            movies.dropna(inplace=True)
            print(f"=========rechecking null values after drop===========\n{movies.isnull().sum()}\n")
            print(f"No. of duplicate columns:{movies.duplicated().sum()}\n")

            movies['geners'] = movies['genres'].apply(convert)
            movies['keywords'] = movies['keywords'].apply(convert)
            movies['cast'] = movies['cast'].apply(convert_cast)
            movies['crew'] = movies['crew'].apply(fetch_director)
            movies['overview'] = movies['overview'].apply(lambda x:x.split())

            #remove spaces
            movies['cast'] = movies['cast'].apply(remove_space)
            movies['crew'] = movies['crew'].apply(remove_space)
            movies['genres'] = movies['genres'].apply(remove_space)
            movies['keywords'] = movies['keywords'].apply(remove_space)

            #print("=========table after applying convert and space removal function===========\n")
            #print(movies.sample(3))

            # Concatinate all
            movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

            new_df = movies.drop(columns=['overview','genres','keywords','cast','crew'])
            #print("=========table after concatination===========\n")
            #print(new_df.head(3))

            new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
            print(new_df.head())

            # Converting to lower case
            new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

            new_df['tags'] = new_df['tags'].apply(perform_stem)

            new_df.to_csv(os.path.join(self.config.root_dir, "train.csv"),index = False)
            logger.info("Data transformations(EDA) performed")

        except Exception as e:
            raise e