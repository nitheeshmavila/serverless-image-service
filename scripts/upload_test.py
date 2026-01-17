import base64
import json
import requests
import sys
from pathlib import Path

# -------- CONFIG --------
API_ID = "cm7x0uvyut" 
STAGE = "dev"
REGION = "us-east-1"

API_URL = f"http://localhost:4566/restapis/{API_ID}/{STAGE}/_user_request_/images"



def upload_image(image_path, user_id, tags):
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Read image and encode to base64
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "user_id": user_id,
        "filename": image_path.name,
        "content_type": "image/jpeg",
        "image_base64": image_base64,
        "tags": tags
    }

    response = requests.post(
        API_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30
    )

    print("Status Code:", response.status_code)

    try:
        print("Response:", json.dumps(response.json(), indent=2))
    except Exception:
        print("Raw Response:", response.text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_test.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    upload_image(
        image_path=image_path,
        user_id="u1",
        tags=["travel", "beach"]
    )
