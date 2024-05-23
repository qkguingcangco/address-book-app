## Installation

1. **Clone repository:**

    ```bash
    git clone https://github.com/qkguingcangco/address-book-app.git
    cd address-book-app
    ```
2. **Set up virtual environment:**

    ```bash
    python -m venv venv OR python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage
1. **Run application on local server using Uvicorn:**
    ```bash
    uvicorn app.main:app --reload
    OR
    python -m uvicorn app.main:app --reload
    OR
    python3 -m uvicorn app.main:app --reload
    ```
2. **View Swagger**:
   Head on over to http://127.0.0.1:8000/docs


# Endpoints

## 1. Create Address
- **Endpoint**: `POST /addresses/`
- **Description**: Creates a new address.
- **Request Body**:
  ```json
  {
    "name": "string",
    "latitude": "float",
    "longitude": "float"
  }
  ```
- **Response**:
  ```json
  {
    "id": "int",
    "name": "string",
    "latitude": "float",
    "longitude": "float"
  }
  ```

## 2. Get Address by ID
- **Endpoint**: `GET /addresses/{address_id}`
- **Description**: Retrieves an address by its ID.
- **Path Parameter**: `address_id` (int)
- **Response**:
  ```json
  {
    "id": "int",
    "name": "string",
    "latitude": "float",
    "longitude": "float"
  }
  ```

## 3. Delete Address by ID
- **Endpoint**: `DELETE /addresses/{address_id}`
- **Description**: Deletes an address by its ID.
- **Path Parameter**: `address_id` (int)
- **Response**:
  ```json
  {
    "id": "int",
    "name": "string",
    "latitude": "float",
    "longitude": "float"
  }
  ```

## 4. Get All Addresses with Pagination
- **Endpoint**: `GET /addresses/`
- **Description**: Retrieves a paginated list of addresses.
- **Query Parameters**: 
  - `page` (int, optional, default=1)
  - `page_size` (int, optional, default=10)
- **Response**:
  ```json
  {
    "current_page": "int",
    "previous_page": "string or null",
    "next_page": "string or null",
    "addresses": [
      {
        "id": "int",
        "name": "string",
        "latitude": "float",
        "longitude": "float"
      },
      ...
    ]
  }
  ```

  ## 5. Get All Addresses within a given distance
  - **Endpoint**: `GET /addresses/within_distance/`
  - **Description**: Retrieves all addresses within a specified distance.
  - **Query Parameters**:
  - `latitude`: float
  - `longitude`: float
  - `distance_km`: float
- **Response**:
```json
[
  {
    "id": "int",
    "name": "string",
    "latitude": "float",
    "longitude": "float"
  }
]
```

## Testing

1. **Install pytest:**

    ```bash
    pip install pytest
    ```

2. **Run pytest:**

    ```bash
    pytest
    ```
