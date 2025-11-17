from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
import os

from database import Base, engine
from dependencies import verify_access_token

# Import ONLY the routes you need
from routes import (
    auth_routes,
    user_routes,
    cons_manager_routes,
    proj_experience_routes
)

load_dotenv()

app = FastAPI()


# -----------------------------------------------------------
# Custom OpenAPI (adds Bearer JWT security globally)
# -----------------------------------------------------------
security_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Project Management API",
        version="1.0.0",
        description="API for Users, Consulting Managers, and Project Experience",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "security" not in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# -----------------------------------------------------------
# Startup Event
# -----------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

    # STATIC_URL = os.getenv("STATIC_URL", "static")
    # os.makedirs(STATIC_URL, exist_ok=True)

    print("✅ Database ready!")
    # print(f"📁 Static folder: {os.path.abspath(STATIC_URL)}")
    print("🚀 Server starting...")


# -----------------------------------------------------------
# CORS
# -----------------------------------------------------------
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------
# Static Files
# -----------------------------------------------------------
# STATIC_URL = os.getenv("STATIC_URL", "static")
# app.mount("/static", StaticFiles(directory=STATIC_URL), name="static")


# -----------------------------------------------------------
# Public & Protected Routes
# -----------------------------------------------------------

# Authentication
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])

# User CRUD
app.include_router(
    user_routes.router,
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(verify_access_token)]
)


app.include_router(
    cons_manager_routes.router,
    prefix="/consulting-manager",
    tags=["Consulting Manager"],
    # dependencies=[Depends(verify_access_token)]
)

# Project Experience CRUD
app.include_router(
    proj_experience_routes.router,
    prefix="/project-experience",
    tags=["Project Experience"],
    # dependencies=[Depends(verify_access_token)]
)
