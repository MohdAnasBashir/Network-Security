# Network Security Threat Detection using Machine Learning

An end-to-end Machine Learning pipeline for phishing website detection built using Python, Scikit-learn, MongoDB, and MLflow. The project follows a modular architecture with separate components for data ingestion, validation, transformation, model training, and experiment tracking.

---

## Features

- Data Ingestion from MongoDB
- Data Validation and Drift Detection
- Data Transformation and Preprocessing
- Multiple ML Model Training
- Hyperparameter Tuning
- MLflow Experiment Tracking
- Modular Training Pipeline
- Custom Logging and Exception Handling
- Production-ready NetworkModel for inference

---

## Tech Stack

- Python
- Scikit-learn
- Pandas
- NumPy
- MongoDB
- MLflow
- YAML
- Git & GitHub

---

## Models Used

- Random Forest Classifier
- Gradient Boosting Classifier
- Logistic Regression
- Decision Tree
- AdaBoost Classifier

---

## Project Structure

```
Network-Security/
│
├── networksecurity/
│   ├── components/
│   ├── constants/
│   ├── entity/
│   ├── logging/
│   ├── pipeline/
│   ├── utils/
│   └── exception/
│
├── data_schema/
├── main.py
├── requirements.txt
└── setup.py
```

---

## Machine Learning Pipeline

```
MongoDB
   │
   ▼
Data Ingestion
   │
   ▼
Data Validation
   │
   ▼
Data Transformation
   │
   ▼
Model Training
   │
   ▼
MLflow Experiment Tracking
   │
   ▼
NetworkModel
```

---

## Results

- Successfully trained multiple classification models.
- Achieved approximately **99% F1-score** on the phishing website dataset.
- Logged experiments, metrics, and trained models using MLflow.

---

## Future Improvements

- FastAPI deployment
- Docker containerization
- CI/CD pipeline
- Cloud deployment (AWS/Azure)
- Model Monitoring

---

## Author

**Mohd Anas Bashir**

GitHub: https://github.com/MohdAnasBashir
