# ZypherAI - Sheikh Muhammad Aarib Azfar

This project implements a simple web application sever(only) for simulating machine learning model predictions with both synchronous and asynchronous (Redis/RQ) processing capabilities.

## Implementation Details

The application is built using FastAPI and provides the following functionality:

1. Synchronous prediction endpoint that processes requests immediately and returns results
2. Asynchronous prediction endpoint that accepts requests and processes them in the background (Redis / rq worker)
3. Status endpoint to check on and retrieve asynchronous prediction results

Uses Redis and RQ (Redis Queue) for more scalable task processing

Tested using requests.http file through Rest Client extension in VS Code

## How to Run

1. Using Docker Compose:
   ```
   docker-compose up --build
   ```

## API Endpoints

### POST /predict

- **Purpose**: Submit a prediction request
- **Request Body**:
  ```json
  {
    "input": "Sample input data for the model"
  }
  ```
- **Synchronous Mode**:
  - Returns prediction result immediately with 200 status code
- **Asynchronous Mode** (with `Async-Mode: true` header):
  - Returns immediately with 202 status code and a prediction ID

### GET /predict/{prediction_id}

- **Purpose**: Retrieve results for an asynchronous prediction
- **Responses**:
  - 200: Prediction completed successfully
  - 400: Prediction is still processing
  - 404: Prediction ID not found

## Design Decisions

1. **FastAPI Selection**: Chosen for its simplicity, built-in async support, and automatic OpenAPI documentation
2. **Redis**:
   - Redis simplicity to check whether the job is completed or not
   - Redis version demonstrates scalability with distributed task queues
3. **Error Handling**: Properly handles error cases with appropriate status codes
4. **Type Annotations**: Used throughout for better code readability and maintenance

## Assumptions

1. The application does not need persistent storage across restarts
2. The mock prediction function is an accurate representation of actual workload

## Alternatives Considered

1. **Celery**: Could be used instead of RQ for more complex task scheduling
2. **Database Storage**: Could replace in-memory dictionaries for persistence



Sheikh Muhammad Aarib Azfar submission for Sych SDE 2025 Assessment ONLY, it is requested to only share/use for it intented purpose. 