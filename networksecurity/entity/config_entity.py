from datetime import datetime
import os
from networksecurity.constants import training_pipeline


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.timestamp:str=timestamp


class DataIngestionConfig:
    
    def __init__(self,training_pipeline_Config:TrainingPipelineConfig):
        # Store the path of the data_ingestion folder
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_Config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME)
        # Store the path where the complete dataset will be saved
        self.feature_store_file_path:str=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
        # Store the path where train.csv will be save
        self.training_file_path:str=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE_NAME)
        # Store the path where test.csv will be saved
        self.testing_file_path:str=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME)
        # Store the train-test split ratio (20% test data)
        self.train_test_split_ratio:float=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        # Store the MongoDB collection name
        self.collection_name:str=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        # Store the MongoDB database name
        self.database_name:str=training_pipeline.DATA_INGESTION_DATABASE_NAME

        
        