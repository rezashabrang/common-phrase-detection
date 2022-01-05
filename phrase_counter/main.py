"""Customizing fast api."""
from typing import Union

import os

from fastapi import FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi
from routers import http_doc_processor

app = FastAPI()
description = """
API for handling common phrase detection functionalities.
"""


async def get_token_header(x_token: str = Header(...)) -> Union[None, Exception]:
    """."""
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return None


def custom_openapi():
    """Defining custom API schema."""
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


app.openapi = custom_openapi  # type: ignore

app.include_router(
    http_doc_processor.router,
    prefix=os.getenv("ROOT_PATH", ""),
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
