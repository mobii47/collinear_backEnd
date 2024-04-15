import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import MagicMock, patch

client = TestClient(app)


@pytest.fixture
def mock_session_local():
    with patch("your_main_module.SessionLocal") as mock_session_local:
        yield mock_session_local


@pytest.fixture
def mock_list_datasets():
    with patch("your_main_module.list_datasets") as mock_list_datasets:
        yield mock_list_datasets


def test_dataset_not_valid(mock_session_local):
    mock_session_local.return_value = MagicMock()
    response = client.get("/dataset-not-valid/")
    assert response.status_code == 200  # Assuming API responds successfully
    assert (
        "response_data" in response.json()
    )  # Replace "response_data" with the expected response data


def test_dataset_valid(mock_session_local):
    mock_session_local.return_value = MagicMock()
    response = client.get("/dataset-valid/")
    assert response.status_code == 200  # Assuming API responds successfully
    assert (
        "response_data" in response.json()
    )  # Replace "response_data" with the expected response data


# Similar tests for other endpoints can be implemented in a similar way


def test_get_datasets(mock_list_datasets):
    mock_list_datasets.return_value = [
        "dataset1",
        "dataset2",
    ]  # Assuming list_datasets returns some datasets
    response = client.get("/datasets/")
    assert response.status_code == 200
    assert response.json() == {"datasets": ["dataset1", "dataset2"]}


def test_get_datasets_limit(mock_list_datasets):
    mock_list_datasets.return_value = [
        "dataset1",
        "dataset2",
        "dataset3",
    ]  # Assuming list_datasets returns some datasets
    response = client.get("/datasets-10/")
    assert response.status_code == 200
    assert response.json() == {
        "datasets": ["dataset1", "dataset2", "dataset3"][:10]
    }  # Assuming we limit to 10 datasets

