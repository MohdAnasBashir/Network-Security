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


'''DATA VALIDATION'''
class DataValidationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        ##create the directory of validation underartifacts
        self.data_validation_dir:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path:str=os.path.join(self.valid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str=os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path:str=os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str=os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path:str=os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIADATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIADTION_DRIFT_REPORT_FILE_NAME
        )


'''DATA TRANSFORMATION CONFIGURATION transformed train file amd test file path and objevct file path'''
class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME )
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"), )
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)   
        
'''Model Trainer configuration '''
class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, 
            training_pipeline.MODEL_FILE_NAME
        )
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD