from typing import Optional
from pathlib import Path

import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template

from flashcards_htmx.private_components import MockDeck, MockCard


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()



class EmptyDeck:
	def __init__(self):
		self.id = None
		self.name = ""
		self.desc = ""
		self.algorithm = None


class EmptyCard:
	def __init__(self):
		self.id = None
		self.question = ""
		self.answer = ""


@router.get("/home", response_class=HTMLResponse)
async def home_page(render = Depends(template('private/home.html'))):
	return render(navbar_title="Home", searchable=True)


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(render = Depends(template('private/profile.html'))):
	return render(navbar_title="My name")


@router.get("/study/{deck_id}", response_class=HTMLResponse)
async def study_page(deck_id: str, render = Depends(template('private/study.html'))):
	deck = MockDeck(deck_id)
	return render(navbar_title=deck.name, deck=deck)
		

@router.get("/decks/new", response_class=HTMLResponse)
async def create_deck_page(render = Depends(template('private/deck.html'))):
	return render(navbar_title="New Deck", deck=EmptyDeck())
		

@router.get("/decks/{deck_id}", response_class=HTMLResponse)
async def edit_deck_page(deck_id: str, render = Depends(template('private/deck.html'))):
	deck = MockDeck(deck_id)
	return render(navbar_title=deck.name, deck=deck)


@router.post("/decks/{deck_id}", response_class=RedirectResponse)
async def save_deck_endpoint(deck_id: Optional[str], request: Request):
	if not deck_id:
		# FIXME CREATE NEW DECK
		pass
	else:
		# FIXME SAVE CHANGES
		pass
	return RedirectResponse(request.url_for('home_page'), status_code=status.HTTP_302_FOUND)
		

@router.get("/decks/{deck_id}/cards", response_class=HTMLResponse)
async def cards_page(deck_id: str, render = Depends(template('private/cards.html'))):
	deck = MockDeck(deck_id)
	return render(navbar_title=deck.name, deck=deck, searchable=True)


@router.get("/decks/{deck_id}/cards/new", response_class=HTMLResponse)
async def create_card_page(deck_id: str, render = Depends(template('private/card.html'))):
	deck = MockDeck(deck_id)
	return render(navbar_title=deck.name, deck=deck, card=EmptyCard())


@router.get("/decks/{deck_id}/cards/{card_id}", response_class=HTMLResponse)
async def edit_card_page(deck_id: str, card_id: str, render = Depends(template('private/card.html'))):
	deck = MockDeck(deck_id)
	card = MockCard(card_id)
	return render(navbar_title=deck.name, deck=deck, card=card)


@router.post("/decks/{deck_id}/cards/{card_id}", response_class=RedirectResponse)
async def save_card_endpoint(deck_id: str, card_id: Optional[str], request: Request):
	if not card_id:
		# FIXME CREATE NEW DECK
		pass
	else:
		# FIXME SAVE CHANGES
		pass
	return RedirectResponse(request.url_for('home_page'), status_code=status.HTTP_302_FOUND)
		

@router.post("/logout", response_class=RedirectResponse)
async def logout_page(request: Request):
	return RedirectResponse(request.url_for('home_page'), status_code=status.HTTP_302_FOUND)

	
