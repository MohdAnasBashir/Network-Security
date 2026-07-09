import os
import sys
import pymongo
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_Array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_data_transformer_object(cls)->Pipeline:
        """
        Creates a KNNImputer to fill missing (NaN) values.
        The KNNImputer uses the settings defined in training_pipeline.py.
        It then puts the KNNImputer inside a Pipeline and returns that Pipeline.
        Args:
            cls: The DataTransformation class.
        Returns:
            A Pipeline object containing the KNNImputer.
        """
        logging.info("enetered get data trandformer object method")

        try:
            #** means parameter  are being considered as dictionary'
            #key-value parametrs because of **
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialise knnimputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline=Pipeline([("imputer",imputer)])

            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("enetered initiate data tarsnformation of data transformation class")

        try:
            ##step1 read the train and test data valid coming from 
            ##data validation artifact
            logging.info("Starting Data Transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            ##now we have readed the train and test file recioebved from data validation artifact

            ##step2

            ##training dataframe remove the target feature and target feature from train
            ##TRAINING DATA
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            ##now we know that there are many entries as -1 replace with 0
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            ##TESTINGDATA
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            ##now we know that there are many entries as -1 replace with 0
            target_feature_test_df=target_feature_test_df.replace(-1,0)


            ##step 3 apply knn imputer to handle nan values
            preprocessor=self.get_data_transformer_object()
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)

            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)

            ##step4
            train_arr=np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]



            ##step5 save nupmy array data
            save_numpy_Array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_Array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            ##step6 save the object
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)

            ##step7 preparing artifacts
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
