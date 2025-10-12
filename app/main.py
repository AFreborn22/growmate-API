import logging
import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.endpoint import auth
from app.endpoint import agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("myapp")

app = FastAPI(
    title="GrowMate API",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "docExpansion": "none",
    },
)

@app.middleware("http")
async def logRequests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# schema = app.openapi()
# schema.setdefault("security", [{"HTTPBearer": []}])
# app.openapi_schema = schema
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET, POST, PUT, DELETE"],  
    allow_headers=["*"], 
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(agent.router, prefix="/api/agent", tags=["chat"])