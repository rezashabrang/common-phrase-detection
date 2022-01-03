""" Document processor Endpoint """
from fastapi import APIRouter, HTTPException, Path
from lib.phrase_detector import phrase_counter
from lib.db import integrate_phrase_data


# ------------------------------ Initialization -------------------------------
router = APIRouter()

# ---------------------------- function definition ----------------------------


@router.get(
    "/api/doc-process/{doc}",
    response_model=dict,
    tags=['Document Process'],
    status_code=201
)
async def read_items(
        doc: str = Path(
            ...,
            title="Input document text",
        ),
):
    """Getting document content, processing & saving results in db."""
    try:
        phrase_count_res = phrase_counter(doc)
        db_res = integrate_phrase_data(phrase_count_res)
        # print(db_res)
        if db_res:
            res = {
                "message": "Results integration done."
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="Nothing to integrate. Perhaps an empty doc was passed!"
            )
        return res

    except HTTPException as err:
        raise HTTPException from err

    except Exception as err:
        print(err)
        raise HTTPException(status_code=400) from err
