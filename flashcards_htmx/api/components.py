from random import randint
from pathlib import Path
import datetime
import shelve

from jinja2 import Template
import starlette.status as status
from fastapi import APIRouter, Request, Depends, HTTPException
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
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        
        card_templates = db["templates"]
        for card in deck["cards"].values():
            card["rendered_preview"] = Template(card_templates[card["type"]]["preview"]).render(**card["data"])
    return render(deck=deck, deck_id=deck_id)


@router.get("/decks/{deck_id}/study", response_class=HTMLResponse)
async def study_component(
    deck_id: str, render=Depends(template("responses/study.html"))
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        
        if not len(deck["cards"]):
            return render(card=None, deck_id=deck_id)

        # TODO actually get the card to study from the deck
        card_id = randint(1, len(deck["cards"]))
        # if card_id == "1":
        #     return render(error="Test Error")
    
        card = deck["cards"].get(str(card_id), {})
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        
        card["rendered_question"] = Template(db["templates"][card["type"]]["question"]).render(**card["data"]["question"])
        card["rendered_answer"] = Template(db["templates"][card["type"]]["answer"]).render(**card["data"]["answer"])
    
    return render(deck=deck, deck_id=deck_id, card=deck["cards"][str(card_id)], card_id=str(card_id))


@router.post(
    "/decks/{deck_id}/study/{card_id}/{result}", response_class=RedirectResponse
)
async def save_review_component(
    deck_id: str, card_id: str, result: str, request: Request
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        
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
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        card = deck["cards"].get(card_id, {})
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        card_templates = db["templates"]
    return render(
        title=f"Deleting card",
        content=f"<p>Are you really sure you wanna delete this card?</p><br>" + Template(card_templates[card["type"]]["preview"]).render(**card["data"]),
        positive=f"Yes, delete it",
        negative=f"No, don't delete",
        delete_endpoint="delete_card_endpoint",
        endpoint_params={"deck_id": deck_id, "card_id": card_id},
    )
