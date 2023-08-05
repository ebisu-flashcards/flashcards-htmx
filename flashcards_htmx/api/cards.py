from typing import Optional
from pathlib import Path
import shelve

from jinja2 import Template
import starlette.status as status
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template, database


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/decks/{deck_id}/cards", response_class=HTMLResponse)
async def cards_page(
    deck_id: str, request: Request, render=Depends(template("private/cards.html"))
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
    return render(
        navbar_title=deck["name"],
        deck=deck,
        deck_id=deck_id,
        searchable=True,
        new_item_endpoint=request.url_for("create_card_page", deck_id=deck_id),
        new_item_text="New Card...",
    )


@router.get("/htmx/components/decks/{deck_id}/cards", response_class=HTMLResponse)
async def cards_component(
    deck_id: str, render=Depends(template("responses/cards.html"))
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")

        card_templates = db["templates"]
        for card in deck["cards"].values():
            card["rendered_preview"] = Template(
                card_templates[card["type"]]["preview"]
            ).render(**card["data"])
    return render(deck=deck, deck_id=deck_id)


@router.get("/decks/{deck_id}/cards/new", response_class=HTMLResponse)
async def create_card_page(deck_id: str, render=Depends(template("private/card.html"))):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")

        id = len(db["decks"].get(deck_id, {}).get("cards", {})) + 1
        card_templates = db["templates"]
        for template in card_templates.values():
            template["rendered_form"] = Template(template["form"]).render(
                question={}, answer={}, preview={}
            )
    return render(
        navbar_title=deck["name"],
        deck=deck,
        deck_id=deck_id,
        card={
            "id": id,
            "data": {
                "question": {},
                "answer": {},
                "preview": {},
            },
            "tags": [],
            "reviews": {},
        },
        card_id=id,
        card_templates=card_templates,
    )


@router.get("/decks/{deck_id}/cards/{card_id}", response_class=HTMLResponse)
async def edit_card_page(
    deck_id: str, card_id: str, render=Depends(template("private/card.html"))
):
    with shelve.open(database) as db:
        deck = db["decks"].get(deck_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")

        card_templates = db["templates"]
        card = deck["cards"].get(card_id, {})
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        for template in card_templates.values():
            template["rendered_form"] = Template(template["form"]).render(
                **card["data"]
            )

    return render(
        navbar_title=deck["name"],
        deck=deck,
        deck_id=deck_id,
        card=card,
        card_id=card_id,
        card_templates=card_templates,
    )


@router.post("/decks/{deck_id}/cards/{card_id}", response_class=RedirectResponse)
async def save_card_endpoint(deck_id: str, card_id: Optional[str], request: Request):
    async with request.form() as form:
        with shelve.open(database) as db:
            deck = db["decks"].get(deck_id, {})
            deck["cards"][card_id] = {
                **deck["cards"].get(card_id, {"reviews": {}}),
                "data": {
                    "question": {
                        key[len("question.") :]: value
                        for key, value in form.items()
                        if key.startswith("question.")
                    },
                    "answer": {
                        key[len("answer.") :]: value
                        for key, value in form.items()
                        if key.startswith("answer.")
                    },
                    "preview": {
                        key[len("preview.") :]: value
                        for key, value in form.items()
                        if key.startswith("preview.")
                    },
                },
                "tags": [tag.strip() for tag in form["tags"].split(",") if tag.strip()],
                "type": form["type"],
            }

    return RedirectResponse(
        request.url_for("cards_page", deck_id=deck_id),
        status_code=status.HTTP_302_FOUND,
    )


@router.get(
    "/htmx/components/decks/{deck_id}/cards/{card_id}/confirm-delete",
    response_class=HTMLResponse,
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
        content=f"<p>Are you really sure you wanna delete this card?</p><br>"
        + Template(card_templates[card["type"]]["preview"]).render(**card["data"]),
        positive=f"Yes, delete it",
        negative=f"No, don't delete",
        delete_endpoint="delete_card_endpoint",
        endpoint_params={"deck_id": deck_id, "card_id": card_id},
    )


@router.get("/decks/{deck_id}/cards/{card_id}/delete", response_class=RedirectResponse)
async def delete_card_endpoint(
    request: Request,
    deck_id: str,
    card_id: str,
):
    with shelve.open(database) as db:
        if deck_id not in db["decks"]:
            raise HTTPException(status_code=404, detail="Deck not found")
        if card_id not in db["decks"][deck_id]["cards"]:
            raise HTTPException(status_code=404, detail="Card not found")
        del db["decks"][deck_id]["cards"][card_id]

    return RedirectResponse(
        request.url_for("cards_page", deck_id=deck_id),
        status_code=status.HTTP_302_FOUND,
    )
