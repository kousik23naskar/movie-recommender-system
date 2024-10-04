from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_ingestion import DataIngestion
from src.mlProject.logging import logger



STAGE_NAME = "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        #config = ConfigurationManager()
        #data_ingestion_config = config.get_data_ingestion_config()
        #data_ingestion = DataIngestion(config=data_ingestion_config)
        config = ConfigurationManager().get_data_ingestion_config()
        data_ingestion = DataIngestion(config=config)
        data_ingestion.download_file()

        if data_ingestion.is_tar_gz_file():
            data_ingestion.extract_tar_gz_file()
        elif data_ingestion.is_zip_file():
            data_ingestion.extract_zip_file()
        else:
            logger.error(f"Unsupported file format: {data_ingestion.config.local_data_file}")


    
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e