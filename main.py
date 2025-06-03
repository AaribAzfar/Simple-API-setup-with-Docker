# Sheikh Muhammad Aarib Azfar SDE Sych 2025 Assessment

import time
import random
import uuid
import json
from typing import Dict, Optional
from fastapi import FastAPI, Header, HTTPException, Response
from pydantic import BaseModel
import uvicorn
import redis
from rq import Queue
from rq.job import Job

# response structures
class PredictionRequest(BaseModel):
    input: str

class AsyncPredictionResponse(BaseModel):
    message: str
    prediction_id: str

class PredictionResult(BaseModel):
    prediction_id: str
    output: Dict[str, str]

class ErrorResponse(BaseModel):
    error: str

# Mock function as provided in the assessment
def mock_model_predict(input: str) -> Dict[str, str]:
    time.sleep(random.randint(10, 17))  # Simulate processing delay
    result = str(random.randint(1000, 20000))
    output = {"input": input, "result": result}
    return output

#Redis connection and queue
redis_conn = redis.Redis(host='redis', port=6379, db=0)
prediction_queue = Queue(connection=redis_conn)

# FastAPI application
app = FastAPI(title="ZypherAI - Aarib Azfar")

@app.post("/predict")
async def predict(
    request: PredictionRequest, 
    response: Response,
    async_mode: Optional[str] = Header(None, alias="Async-Mode")
):
    # Check if async mode is requested
    if async_mode and async_mode.lower() == "true":
        # Generate a unique prediction ID
        prediction_id = str(uuid.uuid4())
        
        # Queue the prediction job
        job = prediction_queue.enqueue(
            mock_model_predict, 
            request.input,
            job_id=prediction_id
        )
        
        # (Accepted)
        response.status_code = 202
        
        # Return immediately with 202 status code
        return AsyncPredictionResponse(
            message="Request received. Processing asynchronously.",
            prediction_id=prediction_id
        )
    else:
        # Synchronous processing
        result = mock_model_predict(request.input)
        return result

@app.get("/predict/{prediction_id}")
async def get_prediction(prediction_id: str, response: Response):
    # Try to fetch the job
    try:
        job = Job.fetch(prediction_id, connection=redis_conn)
    except:
        # Job not found
        response.status_code = 404
        return ErrorResponse(error="Prediction ID not found.")
    
    # Check job status
    if not job.is_finished:
        response.status_code = 400
        return ErrorResponse(error="Prediction is still being processed.")
    
    # Return the result
    return PredictionResult(
        prediction_id=prediction_id,
        output=job.result
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)