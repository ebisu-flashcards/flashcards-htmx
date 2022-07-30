from pathlib import Path

import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/home", response_class=HTMLResponse)
async def home_page(render = Depends(template('private/home.html'))):
	return render(navbar_title="Home")


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(render = Depends(template('private/profile.html'))):
	return render(navbar_title="My name")


@router.get("/study/{deck_id}", response_class=HTMLResponse)
async def study_page(deck_id: str, render = Depends(template('private/study.html'))):
	return render(navbar_title=f"{deck_id}")
		

@router.get("/decks/{deck_id}", response_class=HTMLResponse)
async def edit_deck_page(deck_id: str, render = Depends(template('private/deck.html'))):
	return render(navbar_title=f"{deck_id}")
		

@router.post("/decks/{deck_id}", response_class=RedirectResponse)
async def save_deck_endpoint(deck_id: str, request: Request):
	# FIXME save the deck data!!
	return RedirectResponse(request.url_for('home_page'), status_code=status.HTTP_302_FOUND)
		

@router.get("/decks/{deck_id}/cards", response_class=HTMLResponse)
async def cards_page(deck_id: str, render = Depends(template('private/cards.html'))):
	return render(navbar_title=f"{deck_id}")


@router.get("/decks/{deck_id}/cards/{card_id}", response_class=HTMLResponse)
async def edit_card_page(deck_id: str, render = Depends(template('private/card.html'))):
	return render(navbar_title=f"{deck_id}")


@router.post("/logout", response_class=RedirectResponse)
async def logout_page(request: Request):
	return RedirectResponse(request.url_for('home_page'), status_code=status.HTTP_302_FOUND)

	
