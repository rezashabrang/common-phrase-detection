""" Document processor Endpoint """
from fastapi import APIRouter, HTTPException
from lib.phrase_detector import phrase_counter
from lib.db import integrate_phrase_data
from pydantic import BaseModel
from typing import Dict

# ------------------------------ Initialization -------------------------------
router = APIRouter()

# ---------------------------- function definition ----------------------------


class HtmlFile(BaseModel):
    """Schema for payload."""
    file: str


@router.post(
    "/api/doc-process/",
    response_model=dict,
    tags=['Document Process'],
    status_code=201
)
async def read_items(
        doc: HtmlFile
) -> Dict[str, str]:
    """Getting document content, processing & saving results in db."""
    try:
        doc_content = doc.file
        phrase_count_res = phrase_counter(doc_content)
        integrate_phrase_data(phrase_count_res)

        res = {
            "message": "Results integration done."
        }
        return res

    except HTTPException as err:
        raise HTTPException(
            status_code=400
        ) from err

    except Exception as err:
        raise HTTPException(status_code=400) from err
