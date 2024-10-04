from src.mlProject.config.configuration import ConfigurationManager
from src.mlProject.components.model_prediction import ModelPrediction
from src.mlProject.logging import logger



STAGE_NAME = "Model Prediction stage"

class ModelPredictionPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_prediction_config = config.get_model_prediction_config()
        model_prediction_config = ModelPrediction(config=model_prediction_config)
        model_prediction_config.recommend("Spider-Man 2")




if __name__ == '__main__':
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        obj = ModelPredictionPipeline()
        obj.main()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e