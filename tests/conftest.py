import pytest
import requests
import base64
from pathlib import Path

API_ID = "cm7x0uvyut"
STAGE = "dev"

BASE_URL = f"http://localhost:4566/restapis/{API_ID}/{STAGE}/_user_request_"


@pytest.fixture(scope="session")
def api_base_url():
    # Ensure LocalStack is running
    try:
        requests.get("http://localhost:4566")
    except Exception:
        pytest.exit("LocalStack is not running")

    return BASE_URL


@pytest.fixture(scope="session")
def uploaded_image_id(api_base_url):
    """
    Upload one image once and reuse it across tests
    """
    image_path = Path("tests/sample.jpg")

    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()
    payload = {
        "user_id": "test_user",
        "filename": "sample.jpg",
        "content_type": "image/jpeg",
        "image_base64": image_base64,
        "tags": ["test", "pytest"]
    }

    response = requests.post(
        f"{api_base_url}/images",
        json=payload,
        timeout=30
    )
    assert response.status_code == 201
    return response.json()["image_id"]
