from networksecurity.components.data_ingestion import DataIngestion
import sys
from networksecurity.logging.logger import logging
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.pipeline.training_pipeline import TrainingPipeline
if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate data ingestion")

        dataingestionartifact=dataingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("data Initiation completed")

        ##data validation
        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        datavalidation=DataValidation(dataingestionartifact,datavalidationconfig)
        logging.info("initiated te edata validation")
        data_validation_artifact=datavalidation.initiate_data_validation()
        logging.info("data validation completed")
        print(data_validation_artifact)


        ##data transformation
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)


        ##mode;l trainer
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        modeltrainer=ModelTrainer(data_transformation_artifact,model_trainer_config)
        model_trainer_artifact=modeltrainer.initiate_model_trainer()
        print(model_trainer_artifact)

       

       


    except Exception as e:
        raise NetworkSecurityException(e,sys)