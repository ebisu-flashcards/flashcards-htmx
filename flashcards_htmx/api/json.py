import shelve
import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse

from flashcards_htmx.app import template, database


router = APIRouter()


@router.get("/export/{deck_id}", response_class=FileResponse)
async def export_deck_endpoint(request: Request):
    with shelve.open(database) as db:
        deck = db["decks"].get(request.path_params["deck_id"], {})
        if not deck:
            return JSONResponse(status_code=404, content={"message": "Item not found"})
        path = f"tmp/{deck}.json"

    return FileResponse(path)

