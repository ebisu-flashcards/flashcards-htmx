from random import randint
from pathlib import Path

import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter(prefix='/_components')


class MockDeck:
	def __init__(self, index):
		self.id = str(index)
		self.name = f"Deck Deck Deck Deck Deck Deck N. {index}"
		self.desc = f"Description for deck n. {index}"
		self.algorithm = "Random"


class MockCard:
	def __init__(self, index):
		self.id = str(index)
		self.question = f"Question N. {index}"
		self.answer = f"Answer n. {index}"


@router.get("/decks", response_class=HTMLResponse)
async def decks_component(render = Depends(template('responses/decks.html'))):
	return render(decks=[MockDeck(i) for i in range(4)])


@router.get("/decks/search_filters", response_class=HTMLResponse)
async def decks_search_component(render = Depends(template('components/filter-modal.html'))):
	return render(
		title=f"Filters", 
		content=f"Content here",
		positive=f"Search",
		negative=f"Cancel"
	)
	

@router.get("/decks/{deck_id}/cards", response_class=HTMLResponse)
async def cards_component(deck_id: str, render = Depends(template('responses/cards.html'))):
	return render(deck=MockDeck(deck_id), cards=[MockCard(i) for i in range(20)])


@router.get("/decks/{deck_id}/study", response_class=HTMLResponse)
async def study_component(deck_id: str, render = Depends(template('responses/study.html'))):
	card_id = randint(0, 10)
	if deck_id == "0":
		return render(card=None)
	if deck_id == "1":
		return render(error="Test Error")
	return render(deck=MockDeck(deck_id), card=MockCard(card_id))


@router.post("/decks/{deck_id}/study/{card_id}/{result}", response_class=RedirectResponse)
async def save_review_component(deck_id: str, card_id: str, result: str, request: Request):
	# FIXME save the review
	deck = MockDeck(deck_id)
	return RedirectResponse(request.url_for('study_component', deck_id=deck.id), status_code=status.HTTP_302_FOUND)




@router.get("/decks/{deck_id}/confirm-delete", response_class=HTMLResponse)
async def deck_confirm_delete_component(deck_id: str, render = Depends(template('components/message-modal.html'))):
	deck = MockDeck(deck_id)
	return render(
		title=f"Deleting {deck.name}", 
		content=f"Are you really sure you wanna delete the deck {deck.name}? It contains XXXX cards!",
		positive=f"Yes, delete {deck.name}",
		negative=f"No, don't delete"
	)


@router.get("/decks/{deck_id}/cards/{card_id}/confirm-delete", response_class=HTMLResponse)
async def card_confirm_delete_component(deck_id: str, card_id: str, render = Depends(template('components/message-modal.html'))):
	return render(
		title=f"Deleting card", 
		content=f"Are you really sure you wanna delete this card?",
		positive=f"Yes, delete it",
		negative=f"No, don't delete"
	)


