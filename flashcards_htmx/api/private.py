from pathlib import Path
from random import randint
import shelve

from jinja2 import Template
import starlette.status as status
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template, database


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(render=Depends(template("private/profile.html"))):
    return render(navbar_title="Settings")


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
            return render(card=None, deck_id=deck_id)

        # TODO actually get the card to study from the deck
        card_id = randint(1, len(deck["cards"]))
        # if card_id == "1":
        #     return render(error="Test Error")

        card = deck["cards"].get(str(card_id), {})
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        card["rendered_question"] = Template(
            db["templates"][card["type"]]["question"]
        ).render(**card["data"]["question"])
        
        card["rendered_answer"] = Template(
            db["templates"][card["type"]]["answer"]
        ).render(**card["data"]["answer"])

    return render(
        deck=deck,
        deck_id=deck_id,
        card=deck["cards"][str(card_id)],
        card_id=str(card_id),
    )


@router.post(
    "/htmx/components/decks/{deck_id}/study/{card_id}/{result}",
    response_class=RedirectResponse,
)
async def save_review_component(
    deck_id: str, card_id: str, result: str, request: Request
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")

        # TODO save meaningful review data
        # deck["cards"][card_id]["reviews"][len(deck["cards"][card_id]["reviews"])] = {
        #     "date": datetime.datetime.utcnow().isoformat(),
        #     "result": result,
        # }
    return RedirectResponse(
        request.url_for("study_component", deck_id=deck_id),
        status_code=status.HTTP_302_FOUND,
    )


@router.post("/logout", response_class=RedirectResponse)
async def logout_page(request: Request):
    return RedirectResponse(
        request.url_for("home_page"), status_code=status.HTTP_302_FOUND
    )
