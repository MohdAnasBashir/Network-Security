import os
import sys
import pymongo
import numpy as np
import pandas as pd
from typing import List
from scipy.stats import ks_2samp
#input is coming from data ingestion artifact
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from sklearn.model_selection import train_test_split
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
##initial info
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    ##read the data from file path and return as csv
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    ##it will be returning true or false
    def validation_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            ##now we need to checcck schema 
            no_of_columns = len(self._schema_config["columns"])
            logging.info(f"required no of columns{no_of_columns}")
            logging.info(f"data frame has columns:{len(dataframe.columns)}")
            ##compare lengths
            if(len(dataframe.columns)==no_of_columns):
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True

            report={}

            for column in base_df.columns:
                ##compare distribution for each column
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                # print(column, is_same_dist.pvalue)
                if threshold <=is_same_dist.pvalue:
                    #no change in distribution
                    is_found=False
                else:
                    is_found=True
                    status=False##means datadrift happened
                report.update(
                    {
                        column:{
                            "p_value":float(is_same_dist.pvalue),
                            "drift_status":is_found
                        }
                    }
                )
            drift_report_file_path=self.data_validation_config.drift_report_file_path

            ##create taht directory 
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            ##now we need tpo write this update in reportyaml
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status

        except Exception as e:
            raise NetworkSecurityException(e,sys)





    #now we need to initiate it 
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            ##read the data from teh train anmd test file path
            train_dataframe= self.read_data(train_file_path)
            test_dataframe=self.read_data(test_file_path)

            ##now validating it with no of columns
            #thats with the dataframe we are providing with schema
            status=self.validation_columns(train_dataframe)
            if not status :
                raise Exception("Train dataset does not contain all required columns.")
            
            status=self.validation_columns(test_dataframe)
            if not status :
                raise Exception("Test dataset does not contain all required columns.")
            
            ##lets check data drift
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            ##craete valid train path directory
            if status:
                os.makedirs(
                    os.path.dirname(self.data_validation_config.valid_train_file_path),
                    exist_ok=True
                )
                train_dataframe.to_csv(
                    self.data_validation_config.valid_train_file_path,
                    index=False,
                    header=True
                )
                test_dataframe.to_csv(
                    self.data_validation_config.valid_test_file_path,
                    index=False,
                    header=True
                )
                data_validation_artifact = DataValidationArtifact(
                    validation_status=True,
                    valid_train_file_path=self.data_validation_config.valid_train_file_path,
                    valid_test_file_path=self.data_validation_config.valid_test_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )
            else:
                os.makedirs(
                    os.path.dirname(self.data_validation_config.invalid_train_file_path),
                    exist_ok=True
                )

                train_dataframe.to_csv(
                    self.data_validation_config.invalid_train_file_path,
                    index=False,
                    header=True
                )

                test_dataframe.to_csv(
                    self.data_validation_config.invalid_test_file_path,
                    index=False,
                    header=True
                )

                data_validation_artifact = DataValidationArtifact(
                    validation_status=False,
                    valid_train_file_path=None,
                    valid_test_file_path=None,
                    invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                    invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


