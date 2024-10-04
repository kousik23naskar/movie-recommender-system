import os
from box.exceptions import BoxValueError
import yaml
from src.mlProject.logging import logger
import json
import pickle
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import ast #Abstract Syntax Trees
import nltk
from nltk.stem import PorterStemmer



@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns the contents as a ConfigBox

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Creates directories given a list of directory paths

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            if verbose:
                logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")




@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    pickle.dump(value=data, filename=path)
    #joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = pickle.load(path)
    #data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data



@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

@ensure_annotations
def convert(text) -> list:
    """
    for converting str to list
    """
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L

@ensure_annotations
def convert_cast(text) -> list:
    """
    Just keeping top 3 cast
    """
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L


@ensure_annotations
def fetch_director(text) -> list:
    """
    Fetching director's name
    """
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

@ensure_annotations
def remove_space(L) -> list:
    """
        removing space like:
                'Anna Kendrick'--> 'AnnaKendrick'
        """
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1


ps = PorterStemmer()
@ensure_annotations
def perform_stem(text):
    """
    --Word--            --Stem--            
    program             program             
    programming         program             
    programer           program
    """
    T = []
    
    for i in text.split():
        T.append(ps.stem(i))
    
    return " ".join(T)