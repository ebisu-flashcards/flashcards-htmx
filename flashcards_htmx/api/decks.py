from typing import Optional

from pathlib import Path
import shelve
import json
from copy import deepcopy
from hashlib import md5

import starlette.status as status
from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template, database
from flashcards_htmx.api.algorithms import ALGORITHMS


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request, render=Depends(template("private/home.html"))):
    return render(
        navbar_title="Home",
        searchable=True,
        new_item_endpoint=request.url_for("create_deck_page"),
        upload_item_endpoint=request.url_for("import_deck_page"),
        new_item_text="New Deck...",
    )


@router.get("/htmx/components/decks", response_class=HTMLResponse)
async def decks_component(render=Depends(template("responses/decks.html"))):
    with shelve.open(database) as db:
        return render(decks=db["decks"])


@router.get("/htmx/components/decks/search_filters", response_class=HTMLResponse)
async def decks_search_component(
    render=Depends(template("components/filter-modal.html")),
):
    return render(
        title=f"decks", content=f"Content here", positive=f"Search", negative=f"Cancel"
    )


@router.get("/decks/new", response_class=HTMLResponse)
async def create_deck_page(render=Depends(template("private/deck.html"))):
    return render(
        navbar_title="New Deck",
        deck={"name": "", "description": ""},
        algorithms=ALGORITHMS.keys(),
        deck_id=None
    )


@router.get("/decks/import", response_class=HTMLResponse)
async def import_deck_page(render=Depends(template("private/import.html"))):
    return render(navbar_title="Import Deck")


@router.post("/decks/import", response_class=RedirectResponse)
async def import_deck_endpoint(file: UploadFile):
    try:
        contents = await file.read()
        deck = json.loads(contents)
        with shelve.open(database) as db:
            deck_id = md5(deck["name"].encode()).hexdigest()
            if deck_id in db["decks"]:
                raise HTTPException(status_code=409, detail="Deck with this name already exists")
            db["decks"][deck_id] = deck
                
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error importing the deck",
        )
    finally:
        await file.close()
    return RedirectResponse(
        router.url_path_for("home_page"), status_code=status.HTTP_302_FOUND
    )


@router.get("/decks/{deck_id}/export", response_class=FileResponse)
async def export_deck_endpoint(request: Request):
    with shelve.open(database) as db:
        deck = deepcopy(db["decks"].get(request.path_params["deck_id"], {}))
        if not deck:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        deck["cards"] = {
            card_id: {
                key: val for key, val in card.items() 
                #if not key not in ["preview", "schema_name", "rendered_question", "rendered_answer"]
            }
            for card_id, card in deck["cards"].items()
        }
        path = Path(__file__).parent.parent / f"tmp/{deck['name']}.json"

        with open(path, "w") as file:
            json.dump(deck, file, indent=4)
    return FileResponse(
        path, media_type="application/octet-stream", filename=f"{deck['name']}.json"
    )


@router.get("/decks/{deck_id}", response_class=HTMLResponse)
async def edit_deck_page(deck_id: str, render=Depends(template("private/deck.html"))):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
    return render(navbar_title=deck["name"], deck=deck, deck_id=deck_id, algorithms=ALGORITHMS.keys())


@router.post("/decks/{deck_id}", response_class=RedirectResponse)
async def save_deck_endpoint(request: Request, deck_id: Optional[str] = None):
    async with request.form() as form:
        with shelve.open(database) as db:
            if not deck_id:
                deck_id = md5(form["name"].encode()).hexdigest()
                if deck_id in db["decks"]:
                    raise HTTPException(status_code=409, detail="Deck with this name already exists")

            db["decks"][deck_id] = {
                **db["decks"].get(deck_id, {"cards": {}}),
                "name": form["name"],
                "description": form["description"],
                "tags": [tag.strip() for tag in form["tags"].split(",") if tag.strip()],
                "algorithm": form["algorithm"]
            }
    return RedirectResponse(
        request.url_for("home_page"), status_code=status.HTTP_302_FOUND
    )


@router.get(
    "/htmx/components/decks/{deck_id}/confirm-delete", response_class=HTMLResponse
)
async def deck_confirm_delete_component(
    deck_id: str, render=Depends(template("components/message-modal.html"))
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")

    return render(
        title=f"Deleting deck",
        content=f"Are you really sure you wanna delete the deck '{deck['name']}'? It contains {len(deck['cards'])} cards.",
        positive=f"Yes, delete {deck['name']}",
        negative=f"No, don't delete",
        delete_endpoint="delete_deck_endpoint",
        endpoint_params={"deck_id": deck_id},
    )


@router.get("/decks/{deck_id}/delete", response_class=RedirectResponse)
async def delete_deck_endpoint(request: Request, deck_id: str):
    with shelve.open(database) as db:
        if deck_id not in db["decks"]:
            raise HTTPException(status_code=404, detail="Deck not found")
        del db["decks"][deck_id]

    return RedirectResponse(
        request.url_for("home_page"), status_code=status.HTTP_302_FOUND
    )
