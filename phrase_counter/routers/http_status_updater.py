"""Updating the status of the phrase (highlight, stop) based on input."""
from typing import Dict

from fastapi import APIRouter, HTTPException
from lib.db import update_status

# ------------------------------ Initialization -------------------------------
router = APIRouter()

# ---------------------------- function definition ----------------------------


@router.post(
    "/api/status-updater/{phrase}/{status_code}",
    response_model=dict,
    tags=["Status Updater"],
    status_code=201,
)
async def read_phrase_status(phrase: str, status_code: int) -> Dict[str, str]:
    """Getting phrase & status and updating related record in db.

    **Arguments:** <br>
    * **phrase**: Phrase for which the status must be changed.

    * **status_code**: `0` for **highlight** and `1` for **stop**.
    """
    try:
        if status_code not in [0, 1]:
            raise HTTPException(status_code=400, detail="wrong-code")
        status = "stop" if status_code == 1 else "highlight"
        update_status(phrase=phrase, status=status)
        res = {"message": "Status update successful."}

        return res

    except HTTPException as err:
        if err.detail == "no-phrase":
            raise HTTPException(
                status_code=404,
                detail="No phrase was found, please first insert the phrase.",
            ) from err
        elif err.detail == "wrong-code":
            raise HTTPException(
                status_code=400, detail="Status code not in registered codes."
            ) from err
        else:
            raise HTTPException from err

    except Exception as err:
        raise HTTPException(status_code=400) from err