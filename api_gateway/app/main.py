from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
import httpx
import os

app = FastAPI()

COURSES_IP = os.getenv("COURSES_IP")
SCHEDULE_IP = os.getenv("SCHEDULE_IP")
ENROLLMENT_IP = os.getenv("ENROLLMENT_IP")

services = {
    "courses": COURSES_IP,
    "schedule": SCHEDULE_IP,
    "enrollment": ENROLLMENT_IP 
}

async def forward_request(service_url: str, method: str, path: str, body=None):
    async with httpx.AsyncClient(timeout=None) as client:
        url = f"http://{service_url}{path}"
        response = await client.request(method, url, json=body)
        return response
    
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATH"])
async def gateway(service: str, path: str, request: Request):
    if service not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    service_url = services[service]
    body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None

    response = await forward_request(service_url, request.method, f"/{path}", body)

    print(response.status_code)
    print(response.content)
    
    return Response(content=response.json(), status_code=response.status_code)