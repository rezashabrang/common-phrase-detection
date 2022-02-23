"""Customizing fast api."""
from typing import Union

import os

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi
from routers import http_data_fetcher, http_doc_processor, http_status_updater

app = FastAPI()
DESCRIPTION = """
API for handling common phrase detection functionalities.
Here is what each section provides.
<h3>Document Process</h3>
Here you can pass a HTML text in request body to process it.

The process stages are:

* Fetching all H1-H6 and p tags

* Cleaning text
* Finding bags (from 1 to 5 bags of word)
* Counting the number of occurences in text
* Integrating results in database
(Updating count field of the phrase if already exists, otherwise inserting a
new record)

<h3>Status Updater</h3>
Updates statuses. <br>

Changing the status of a phrase to either **stop** or **highlight**.

<h3>Data Fetcher</h3>
Fetching data from database based on the statuses.
Here you can fetch phrases based on 4 different situation for statuses:

* Stop phrases

* Highlight phrases

* Phrases that have status (either stop or highlight)

* Phrases which statuses are not yet determined



"""


async def get_token_header(x_token: str = Header(...)) -> Union[None, Exception]:
    """."""
    if x_token != os.getenv("API_KEY"):
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return None


def custom_openapi():
    """Defining custom API schema."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Phrase API",
        version="0.0",
        description=DESCRIPTION,
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
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    http_status_updater.router,
    prefix=os.getenv("ROOT_PATH", ""),
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    http_data_fetcher.router,
    prefix=os.getenv("ROOT_PATH", ""),
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
