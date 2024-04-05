Collinear AI Backend
This is the backend component for the Collinear AI application. It provides a RESTful API for user management and dataset manipulation.

Installation

Navigate to the project directory:

cd collinear-ai-backend

Install the required dependencies using Pipenv:

pipenv install

Endpoints:

User Management
1. Register a new user
    URL: /user/register/
    Method: POST
    Parameters:
    email (string, required): Email address of the user.
    password (string, required): Password for the user account.

2. Login user
    URL: /user/login/
    Method: POST
    Parameters:
    email (string, required): Email address of the user.
    password (string, required): Password for the user account.

Dataset Operations:
1. Dataset Validation
    Check if dataset is not valid
    URL: /dataset-not-valid/
    Method: GET
    Description: Checks if a dataset is not valid.

2. Check if dataset is valid
    URL: /dataset-valid/
    Method: GET
    Description: Checks if a dataset is valid.

3. Dataset Information
    Get dataset splits
    URL: /splits/
    Method: GET
    Description: Retrieves information about dataset splits.

4. Get first row of dataset
    URL: /first-row/
    Method: GET
    Description: Retrieves the first row of a dataset.#

5. Get dataset slice
    URL: /dataset-slice/
    Method: GET
    Description: Retrieves a slice of the dataset.

6. Search dataset
    URL: /dataset-search/
    Method: GET
    Description: Searches for a query within the dataset.

7. Get dataset size
    URL: /dataset-size/
    Method: GET
    Description: Retrieves the size of the dataset.

8. Get Parquet files
    URL: /parquet-files/
    Method: GET
    Description: Retrieves Parquet files for the dataset.

9. Dataset Listing
    Get list of datasets
    URL: /datasets/
    Method: GET
    Description: Retrieves a list of available datasets.

10. Get first 10 datasets
    URL: /datasets-10/
    Method: GET
    Description: Retrieves the first 10 datasets.

11. Rotten Tomatoes Dataset
    Get Rotten Tomatoes dataset
    URL: /rotten_tomatoes_dataset/
    Method: GET
    Description: Retrieves the Rotten Tomatoes dataset.

12. Filter Datasets
    Filter datasets
    URL: /datasets-filter/
    Method: GET
    Description: Filters datasets based on specific criteria.

For Testing:

we are using pytest to test the backend which is in FAStAPI 
1. pip install pytest
2. pytest

Additional Notes
    This application relies on environment variables for API authentication and base URL configuration.
    Make sure to replace your_api_token and api_base_url with your actual authentication token and API base URL.
    The requests library is used to interact with the API endpoints.
    Some endpoints require a connection to a database, which is managed by the SessionLocal object.
    Error handling is implemented to handle exceptions and return appropriate HTTP status codes.
    Feel free to explore and utilize these endpoints for dataset management and retrieval. Make sure to handle authentication and authorization properly when integrating with the frontend or other components of your application.Ensure that you have configured the database connection properly in the database.py file.This application uses SQLAlchemy for ORM and FastAPI for creating RESTful APIs.Make sure to set the appropriate environment variables for sensitive information such as database credentials and API tokens.You can update the Pipfile with the required dependencies by adding them manually or using the pipenv command. For example:

    pip install fastapi
    pip install sqlalchemy
    pip install uvicorn
    pip install jwt
    pip install datasets
    pip install pytest
