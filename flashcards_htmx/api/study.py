from pathlib import Path
import shelve

from jinja2 import Template
import starlette.status as status
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template, database
from flashcards_htmx.api.algorithms import ALGORITHMS


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()



@router.get("/study/{deck_id}", response_class=HTMLResponse)
async def study_page(deck_id: str, render=Depends(template("private/study.html"))):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
    return render(navbar_title=deck["name"], deck=deck, deck_id=deck_id)


@router.get("/htmx/components/decks/{deck_id}/study", response_class=HTMLResponse)
async def study_component(
    deck_id: str, render=Depends(template("responses/study.html"))
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")

        if not len(deck["cards"]):
            return render(card_id=None, deck_id=deck_id)

        algorithm = ALGORITHMS[deck["algorithm"]]
        card_id, card_type, question, answer = algorithm.next_card(
            deck, db["schemas"]
        )
        buttons = algorithm.buttons()

    return render(
        deck=deck,
        deck_id=deck_id,
        card_id=str(card_id),
        card_type=card_type,
        question=question,
        answer=answer,
        buttons=buttons
    )


@router.post(
    "/htmx/components/decks/{deck_id}/study/{card_id}/{card_type}/{result}",
    response_class=RedirectResponse,
)
async def save_review_component(
    deck_id: str, card_id: str, card_type: str, result: str, request: Request
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")

        algorithm = ALGORITHMS[deck["algorithm"]]
        algorithm.process_result(deck, card_id, card_type, result)

    return RedirectResponse(
        request.url_for("study_component", deck_id=deck_id),
        status_code=status.HTTP_302_FOUND,
    )

