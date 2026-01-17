import requests
from urllib.parse import urlparse, urlunparse


def _rewrite_localstack_url(url: str) -> str:
    """
    Convert http://localstack:4566/... -> http://localhost:4566/...
    for tests
    """
    parsed = urlparse(url)
    return urlunparse(parsed._replace(netloc="localhost:4566"))


def test_get_image(api_base_url, uploaded_image_id):
    response = requests.get(
        f"{api_base_url}/images/{uploaded_image_id}"
    )

    assert response.status_code == 200

    body = response.json()
    assert "download_url" in body

    download_url = _rewrite_localstack_url(body["download_url"])

    image_response = requests.get(download_url)
    assert image_response.status_code == 200
    assert len(image_response.content) > 0
