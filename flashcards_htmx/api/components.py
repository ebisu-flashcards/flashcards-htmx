from random import randint
from pathlib import Path
import datetime

import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template, decks


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter(prefix="/htmx/components")


@router.get("/decks", response_class=HTMLResponse)
async def decks_component(render=Depends(template("responses/decks.html"))):
    return render(decks=decks)


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
    return render(deck=decks[deck_id])


@router.get("/decks/{deck_id}/study", response_class=HTMLResponse)
async def study_component(
    deck_id: str, render=Depends(template("responses/study.html"))
):
    # TODO actually get the card to study from the deck
    card_id = randint(0, 3)
    if card_id == "0":
        return render(card=None)
    if card_id == "1":
        return render(error="Test Error")
    return render(deck=decks[deck_id], deck_id=deck_id, card=decks[deck_id]["cards"]["1"], card_id="1")


@router.post(
    "/decks/{deck_id}/study/{card_id}/{result}", response_class=RedirectResponse
)
async def save_review_component(
    deck_id: str, card_id: str, result: str, request: Request
):
    # TODO save the review
    decks[deck_id]["cards"][card_id]["reviews"][len(decks[deck_id]["cards"][card_id]["reviews"])] = {
        "date": datetime.utcnow().isoformat(),
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
    return render(
        title=f"Deleting {decks[deck_id]['name']}",
        content=f"Are you really sure you wanna delete the deck {decks[deck_id]['name']}? It contains XXXX cards!",
        positive=f"Yes, delete {decks[deck_id]['name']}",
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
    return render(
        title=f"Deleting card n. {decks[deck_id]['cards'][card_id]['id']}",
        content=f"Are you really sure you wanna delete this card? [TODO show card preview]",
        positive=f"Yes, delete it",
        negative=f"No, don't delete",
    )
