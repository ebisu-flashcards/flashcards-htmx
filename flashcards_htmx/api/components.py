from random import randint
from pathlib import Path
import datetime
import shelve

from jinja2 import Template
import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template, database


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter(prefix="/htmx/components")


@router.get("/decks", response_class=HTMLResponse)
async def decks_component(render=Depends(template("responses/decks.html"))):
    with shelve.open(database) as db:
       return render(decks=db["decks"])


@router.get("/decks/search_filters", response_class=HTMLResponse)
async def decks_search_component(
    render=Depends(template("components/filter-modal.html")),
):
    return render(
        title=f"decks", content=f"Content here", positive=f"Search", negative=f"Cancel"
    )


@router.get("/decks/{deck_id}/cards", response_class=HTMLResponse)
async def cards_component(
    deck_id: str, render=Depends(template("responses/cards.html"))
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        card_templates = db["templates"]
        for card in deck["cards"].values():
            card["preview"] = Template(card_templates[card["type"]]["preview"]).render(**card["data"])
    return render(deck=deck, deck_id=deck_id)


@router.get("/decks/{deck_id}/study", response_class=HTMLResponse)
async def study_component(
    deck_id: str, render=Depends(template("responses/study.html"))
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
    if not len(deck["cards"]):
        return render(card=None)
    
    # if card_id == "1":
    #     return render(error="Test Error")
    
    # TODO actually get the card to study from the deck
    card_id = randint(0, len(deck["cards"]))
    return render(deck=deck, deck_id=deck_id, card=deck["cards"][str(card_id)], card_id=str(card_id))


@router.post(
    "/decks/{deck_id}/study/{card_id}/{result}", response_class=RedirectResponse
)
async def save_review_component(
    deck_id: str, card_id: str, result: str, request: Request
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        deck["cards"][card_id]["reviews"][len(deck["cards"][card_id]["reviews"])] = {
            "date": datetime.datetime.utcnow().isoformat(),
            "result": result,
        }
    return RedirectResponse(
        request.url_for("study_component", deck_id=deck_id),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/decks/{deck_id}/confirm-delete", response_class=HTMLResponse)
async def deck_confirm_delete_component(
    deck_id: str, render=Depends(template("components/message-modal.html"))
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
    return render(
        title=f"Deleting {deck['name']}",
        content=f"Are you really sure you wanna delete the deck {deck['name']}? It contains {len(deck['cards'])} cards.",
        positive=f"Yes, delete {deck['name']}",
        negative=f"No, don't delete",
    )


@router.get(
    "/decks/{deck_id}/cards/{card_id}/confirm-delete", response_class=HTMLResponse
)
async def card_confirm_delete_component(
    deck_id: str,
    card_id: str,
    render=Depends(template("components/message-modal.html")),
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
    return render(
        title=f"Deleting card n. {deck['cards'][card_id]['id']}",
        content=f"Are you really sure you wanna delete this card? [TODO show card preview]",
        positive=f"Yes, delete it",
        negative=f"No, don't delete",
    )
