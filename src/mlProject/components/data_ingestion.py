import os
import urllib.request as request
import zipfile
import tarfile
from src.mlProject.logging import logger
from mlProject.utils.common import get_size
from pathlib import Path
from mlProject.entity.config_entity import (DataIngestionConfig)


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            logger.info("Starting data download...")
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} downloaded successfully! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

    def is_tar_gz_file(self):
        return self.config.local_data_file.endswith('.tar.gz')
    
    def is_zip_file(self):
        return self.config.local_data_file.endswith('.zip')

    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = Path(self.config.unzip_dir)
        os.makedirs(unzip_path, exist_ok=True)
        try:
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                #zip_ref.extractall(path=unzip_path,members=zip_ref.getmembers())
                zip_ref.extractall(unzip_path)
            logger.info(f"zip file extracted successfully to {unzip_path}!")
        except zipfile.BadZipFile as e:
            logger.error("Failed to extract zip file.")
            logger.error(str(e))
            with open(self.config.local_data_file, 'rb') as file:
                content = file.read(100)
                logger.debug(f"First 100 bytes of the file: {content}")
            raise

    def extract_tar_gz_file(self):
        """
        Extracts the tar.gz file into the data directory
        """
        unzip_path = Path(self.config.unzip_dir)
        os.makedirs(unzip_path, exist_ok=True)
        try:
            with tarfile.open(self.config.local_data_file, 'r:gz') as tar_ref:
                tar_ref.extractall(unzip_path)
            logger.info(f"tar.gz file extracted successfully to {unzip_path}!")
        except tarfile.TarError as e:
            logger.error("Failed to extract tar.gz file.")
            logger.error(str(e))
            with open(self.config.local_data_file, 'rb') as file:
                content = file.read(100)
                logger.debug(f"First 100 bytes of the file: {content}")
            raise
  