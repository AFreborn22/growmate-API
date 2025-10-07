from fastapi import FastAPI

from app.endpoint import auth, user

app = FastAPI(
    title="GrowMate API",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "docExpansion": "none",
    },
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/user", tags=["user"])

schema = app.openapi()
schema.setdefault("security", [{"HTTPBearer": []}])
app.openapi_schema = schema
