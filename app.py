##frontend

import sys
import os
import certifi 
ca=certifi.where()

from dotenv import load_dotenv

load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel


client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]


app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#home page

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/train")
async def train_route():
    try:
        # initiate the training pipeline
        training_pipeline=TrainingPipeline()
        training_pipeline.run_pipeline()

        return Response("training succesful")

    except Exception as e:
        raise NetworkSecurityException(e,sys) 
    
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory='./templates')



@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        print("1")
        df = pd.read_csv(file.file)

        print("2")
        preprocessor = load_object("final_models/preprocessor.pkl")

        print("3")
        final_model = load_object("final_models/model.pkl")

        print("4")
        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=final_model
        )

        print("5")
        y_pred = network_model.predict(df)

        print("6")
        df["predicted_columns"] = y_pred

        print("7")
        df.to_csv("prediction_output/output.csv")

        print("8")
        table_html = df.to_html(classes="table table-striped")

        print("9")
        return templates.TemplateResponse(
            request=request,
            name="table.html",
            context={
                "table": table_html
            }
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        raise NetworkSecurityException(e, sys)














if __name__=="__main__":
    app_run(app,host="localhost",port=8000)