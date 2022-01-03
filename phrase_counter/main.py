"""Customizing fast api."""
import os
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Header, HTTPException

from routers import http_doc_processor

app = FastAPI()
description = """
API for handling common phrase detection functionalities.
"""


async def get_token_header(x_token: str = Header(...)):
    """."""
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Phrase API",
        version="0.0",
        description=description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(
    http_doc_processor.router,
    prefix=os.getenv('ROOT_PATH', ''),
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
