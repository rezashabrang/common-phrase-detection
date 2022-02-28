"""Document processor Endpoint."""
from typing import Dict

from fastapi import APIRouter, HTTPException, Query
from lib.db import integrate_phrase_data, prepare_phrase_data
from lib.phrase_detector import phrase_counter
from pydantic import BaseModel

from phrase_counter.logger import get_logger

# ------------------------------ Initialization -------------------------------
router = APIRouter()
logger = get_logger()

# ---------------------------- function definition ----------------------------


class PhraseDocument(BaseModel):
    """Schema for payload in doc-process endpoint."""

    document: str


@router.post(
    "/api/doc-process/",
    response_model=dict,
    tags=["Document Process"],
    status_code=201,
)
async def process_document(
    doc: PhraseDocument, doc_type: str = Query("TEXT", enum=["TEXT", "HTML", "URL"])
) -> Dict[str, str]:
    """Getting document content, processing & saving results in db.

    **Example**: <br>
    ```
    {
        "document" :"<p> hello world </p>
    }
    ```
    """
    try:
        phrase_count_res = phrase_counter(doc=doc.document, doc_type=doc_type)
        phrase_res, edge_res = prepare_phrase_data(phrase_count_res)

        # Insert nodes
        integrate_phrase_data(phrase_res, type_data="vertex")

        # Insert edges
        integrate_phrase_data(edge_res, type_data="edge")

        res = {"message": "Results integration done."}
        return res

    except HTTPException as err:
        logger.error(err)
        raise HTTPException(status_code=400) from err

    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=400) from err
