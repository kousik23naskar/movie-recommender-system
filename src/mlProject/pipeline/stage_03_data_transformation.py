from src.mlProject.config.configuration import ConfigurationManager
from src.mlProject.components.data_transformation import DataTransformation
from src.mlProject.logging import logger
from pathlib import Path




STAGE_NAME = "Data Transformation stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass


    def main(self):
        try:
            with open(Path("artifacts/data_validation/overall_validation_status.txt"), "r") as f:
                status = f.read().split(" ")[-1]
                logger.info(f"====== printing the validation status: {status}  =========")

            if status == "True":
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.perform_data_transformation()

            else:
                raise Exception("You data schema is not valid")

        except Exception as e:
            print(e)





if __name__ == '__main__':
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e