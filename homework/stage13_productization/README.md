# Project Title: Stage 13 Productization Homework

## Project Overview and Objectives
This project demonstrates the productization of a machine learning model. The objective is to take a trained model, clean and modularize the code, and deploy it as a REST API using Flask. This ensures the project is reproducible, scalable, and ready for handoff to other teams.

## How to Rerun Scripts/Notebooks
1.  **Environment Setup**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Notebook**: Open and run the cells in `notebooks/stage13_productization_homework-starter.ipynb` to train and save the model.
3.  **Run API**:
    ```bash
    python app.py
    ```
    The API will be available at `http://127.0.0.1:5000`.

## Assumptions, Risks, and Lifecycle Mapping
* **Assumptions**: The mock model assumes a linear relationship between the features and the target. The input data is expected to be clean and numerical.
* **Risks**: The API currently has no authentication, making it insecure for production use. Error handling is basic and may not cover all edge cases.
* **Lifecycle**: This project is in the "Deployment" phase. Next steps would involve moving to a more robust hosting solution, adding monitoring, and implementing CI/CD pipelines.

## Instructions for Using the API
The API has two prediction endpoints:

1.  `POST /predict`: Sends a JSON payload to get a prediction.
    * **URL**: `http://127.0.0.1:5000/predict`
    * **Method**: `POST`
    * **Body**: `{"features": [[feature1, feature2]]}`
    * **Example**: `curl -X POST -H "Content-Type: application/json" -d '{"features": [[1.5, 2.5]]}' http://127.0.0.1:5000/predict`

2.  `GET /predict/<input1>/<input2>`: Uses URL parameters for prediction.
    * **URL**: `http://127.0.0.1:5000/predict/1.5/2.5`
    * **Method**: `GET`

## Stakeholder Summary
(Attach or link to the stakeholder-ready summary PDF or slide deck from Stage 12 here.)