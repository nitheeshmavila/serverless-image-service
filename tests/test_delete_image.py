import requests


def test_delete_image(api_base_url, uploaded_image_id):
    response = requests.delete(
        f"{api_base_url}/images/{uploaded_image_id}"
    )

    assert response.status_code == 200

    # verify deletion
    response = requests.get(
        f"{api_base_url}/images/{uploaded_image_id}"
    )
    assert response.status_code == 404
