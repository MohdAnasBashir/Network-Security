from networksecurity.components.data_ingestion import DataIngestion
import sys
from networksecurity.logging.logger import logging
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig
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

    except Exception as e:
        raise NetworkSecurityException(e,sys)