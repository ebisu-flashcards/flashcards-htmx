from typing import Optional
from pathlib import Path

import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template, decks


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request, render=Depends(template("private/home.html"))):
    return render(
        navbar_title="Home",
        searchable=True,
        new_item_endpoint=request.url_for("create_deck_page"),
        new_item_text="New Deck...",
    )


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(render=Depends(template("private/profile.html"))):
    # TODO actually get the profile information
    return render(navbar_title="My name")


@router.get("/study/{deck_id}", response_class=HTMLResponse)
async def study_page(deck_id: str, render=Depends(template("private/study.html"))):
    return render(navbar_title=decks[deck_id]["name"], deck=decks[deck_id], deck_id=deck_id)


@router.get("/decks/new", response_class=HTMLResponse)
async def create_deck_page(render=Depends(template("private/deck.html"))):
    return render(
        navbar_title="New Deck",
        deck={"name": "", "description": "", "algorithm": "Random"},
        deck_id= len(decks) + 1
    )


@router.get("/decks/{deck_id}", response_class=HTMLResponse)
async def edit_deck_page(deck_id: str, render=Depends(template("private/deck.html"))):
    return render(navbar_title=decks[deck_id]["name"], deck=decks[deck_id], deck_id=deck_id)


@router.post("/decks/{deck_id}", response_class=RedirectResponse)
async def save_deck_endpoint(deck_id: str, request: Request):
    async with request.form() as form:
        decks[deck_id] = {
            "name": form["name"],
            "description": form["description"],
            "algorithm": form["algorithm"],
            "cards": {},
        }
    return RedirectResponse(
        request.url_for("home_page"), status_code=status.HTTP_302_FOUND
    )


@router.get("/decks/{deck_id}/cards", response_class=HTMLResponse)
async def cards_page(
    deck_id: str, request: Request, render=Depends(template("private/cards.html"))
):
    return render(
        navbar_title=decks[deck_id]["name"],
        deck=decks[deck_id],
        deck_id=deck_id,
        searchable=True,
        new_item_endpoint=request.url_for("create_card_page", deck_id=deck_id),
        new_item_text="New Card...",
    )


@router.get("/decks/{deck_id}/cards/new", response_class=HTMLResponse)
async def create_card_page(deck_id: str, render=Depends(template("private/card.html"))):
    return render(
        navbar_title=decks[deck_id]["name"],
        deck=decks[deck_id],
        deck_id=deck_id,
        card={
            "id": len(decks[deck_id]["cards"]) + 1,
            "question_data": {},
            "answer_data": {},
            "preview_data": {},
            "tags": [],
            "type": "Q/A",
        },
    )


@router.get("/decks/{deck_id}/cards/{card_id}", response_class=HTMLResponse)
async def edit_card_page(
    deck_id: str, card_id: str, render=Depends(template("private/card.html"))
):
    return render(
        navbar_title=decks[deck_id]["name"],
        deck=decks[deck_id],
        deck_id=deck_id,
        card=decks[deck_id]["cards"][card_id]
    )


@router.post("/decks/{deck_id}/cards/{card_id}", response_class=RedirectResponse)
async def save_card_endpoint(deck_id: str, card_id: Optional[str], request: Request):
    async with request.form() as form:
        decks[deck_id]["cards"][card_id] = {
            "question_data": {
                key[len("question."):] : value for key, value in form.items() if key.startswith("question.")
            },
            "answer_data": {
                key[len("answer."):] : value for key, value in form.items() if key.startswith("answer.")
            },
            "preview_data": {
                key[len("preview."):] : value for key, value in form.items() if key.startswith("preview.")
            },
            "tags": form["tags"].split(","),
            "type": form["type"],
        }
    return RedirectResponse(
        request.url_for("home_page"), status_code=status.HTTP_302_FOUND
    )


@router.post("/logout", response_class=RedirectResponse)
async def logout_page(request: Request):
    return RedirectResponse(
        request.url_for("home_page"), status_code=status.HTTP_302_FOUND
    )
