from pathlib import Path

import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter(prefix='/_components')



@router.get("/decks", response_class=HTMLResponse)
async def decks_component(render = Depends(template('responses/decks.html'))):
	return render(decks=range(4))
	

@router.get("/decks/{deck_id}/cards", response_class=HTMLResponse)
async def cards_component(deck_id: str, render = Depends(template('responses/cards.html'))):
	return render(cards=range(20))




# @router.get("/decks/{deck_id}", response_class=HTMLResponse)
# async def deck_component(deck_id: str, render = Depends(template('components/deck.html'))):
# 	return render()



@router.get("/decks/{deck_id}/confirm-delete", response_class=HTMLResponse)
async def deck_confirm_delete_component(deck_id: str, render = Depends(template('components/confirm_modal.html'))):
	return render(
		title=f"Deleting {deck_id}", 
		content=f"Are you really sure you wanna delete the deck named {deck_id}? It contains XXXX cards!"
	)


