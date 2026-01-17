import requests


def test_list_images(api_base_url):
    response = requests.get(
        f"{api_base_url}/images",
        params={"user_id": "test_user"}
    )

    assert response.status_code == 200

    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 1
