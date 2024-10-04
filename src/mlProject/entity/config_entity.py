from dataclasses import dataclass
from pathlib import Path

'''
 Entity: it is return type of a function
 NOTE: variables of different stages of ML life cycle are defined in config.yaml
 Here different classes are defined using "dataclass" for custom return type of a function
'''

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    All_STATUS_FILE: str
    unzip_data_dir1: Path
    unzip_data_dir2: Path
    all_schema1: dict
    all_schema2: dict


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path1: Path
    data_path2: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    movie_model: str
    similarity_model: str
    max_features: int       


@dataclass(frozen=True)
class ModelPredictionConfig:
    movie_model_path: Path
    similarity_model_path: Path