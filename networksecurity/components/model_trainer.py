import os
import sys
import pymongo
import numpy as np
import pandas as pd
from typing import List
from scipy.stats import ks_2samp
#input is coming from data ingestion artifact
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from sklearn.model_selection import train_test_split
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
##initial info
from networksecurity.entity.config_entity import DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import save_numpy_Array_data,save_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data,load_object,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
##model importation
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def train_model(self,X_train,y_train,X_test,y_test):
        try:
            ##models we are gonna use
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            ##their hyper parameter tuning aklong with aparmetrs
            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest": {
                    "n_estimators": [64]
                },

                "Gradient Boosting": {
                    "learning_rate": [0.1],
                    "subsample": [0.8],
                    "n_estimators": [64]
                },

                "AdaBoost": {
                    "learning_rate": [0.1],
                    "n_estimators": [64]
                },
                "Logistic Regression":{}
        
            }
            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,params=params)

            ##get the best model score among all in the report dictionary
            best_model_score = max(model_report.values())

            ##get the best model name
            best_model_name = max(model_report, key=model_report.get)


            ##get the best model
            best_model=models[best_model_name]

            y_train_pred=best_model.predict(X_train)

            ##now use metrics py file 
            classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)

            ##will write afunction to track the ml flow

            y_test_pred=best_model.predict(X_test)

            classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

            ##now load the prepocessor pkl taht we get from data trabnsformation
            preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)


            ##craete selected estimator object
            network_model=NetworkModel(preprocessor=preprocessor,model=best_model)

            save_object(self.model_trainer_config.trained_model_file_path,obj=network_model)


            ##model trainer artifact creation
            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            logging.info(f"Model Triner Artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    #now we will initiate the model training
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            ##step1 load the train and test npy aths are output from data transformation
            train_file_path =self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            ##now load the training array and testiong array
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)


            ##Step2 training amnd testing data split 
            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],#last col
                test_arr[:,:-1],
                test_arr[:,-1]#last col
            )

            ##step3 now models come into picture and we need to apply models on it
            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
