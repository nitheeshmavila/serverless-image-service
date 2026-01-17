
# Serverless Image Service

**serverless backend** for uploading, listing, downloading, and deleting images (Instagram-like), built using **AWS serverless services** and  runnable **locally with LocalStack**.

---

##  Features

- Upload images with metadata
- List images with filters
- Secure image download using **pre-signed S3 URLs**
- Delete images (S3 + DynamoDB cleanup)

--- 

##  API Endpoints

### Upload Image
**POST `/images`**

```json
{
  "user_id": "u1",
  "filename": "photo.jpg",
  "content_type": "image/jpeg",
  "image_base64": "<base64>",
  "tags": ["travel", "beach"]
}
````

**Response**

```json
{
  "image_id": "uuid",
  "message": "Image uploaded successfully"
}
```

---

### List Images

**GET `/images?user_id=u1&tag=travel`**

Filters:

* `user_id` (required)
* `tag`
* `from` (ISO date)
* `to` (ISO date)

---

### Download Image

**GET `/images/{image_id}`**

Returns a short-lived **pre-signed URL**.

```json
{
  "image_id": "uuid",
  "download_url": "https://..."
}
```

---

### Delete Image

**DELETE `/images/{image_id}`**

Deletes the image from S3 and metadata from DynamoDB.

---

##  Local Development (LocalStack)

### Prerequisites

* Docker & Docker Compose
* Python 3.9+
* AWS CLI v2

### Start LocalStack

```bash
docker compose up -d
```

---
