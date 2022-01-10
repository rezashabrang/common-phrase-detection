"Updating the status of the phrase (highlight, stop) based on input."
from fastapi import APIRouter, HTTPException

from lib.db import fetch_data

# ------------------------------ Initialization -------------------------------
router = APIRouter()

# ---------------------------- function definition ----------------------------


@router.get(
    "/api/data-fetcher/",
    response_model=dict,
    tags=['Data Fetcher'],
    status_code=200
)
async def fetch_phrases(
    status: str = None,
    limit: int = 10,
    page: int = 1

):
    """Fetching data from database.

    **Arguments:** <br>

    * **status**: Must be either `highlight`, `stop`, `with_status`, `no_status`
    (leaving it empty will ignore status of the phrase & fetch all available
    data) <br>

        * **highlight**: for fetching highlight phrases.

        * **stop**: for fetching stop phrases.

        * **with_status**: for fetching phrases with status.

        * **no_status**: for fetching phrases that have no status (NULL)
    <br>

    * **limit**: Number of results in a page.

    * **page**: Page number.

    """
    try:
        if status not in [None, "highlight", "stop", "with_status", "no_status"]:
            raise HTTPException(
                status_code=400,
                detail="bad-status"
            )
        offset = (page-1) * limit

        results = fetch_data(
            status=status,
            limit=limit,
            offset=offset
        )

        return {"items": results}
    except HTTPException as err:
        if err.detail == "bad-status":
            raise HTTPException(
                status_code=400,
                detail="Wrong status code input."
            )

    except Exception as err:
        print(err)
        raise HTTPException(status_code=400) from err
