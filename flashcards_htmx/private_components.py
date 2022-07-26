from pathlib import Path

import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/show/decks", response_class=HTMLResponse)
async def decks_component(render = Depends(template('responses/decks.html'))):
	return render(decks=range(4))
	


@router.get("/show/{deck_id}", response_class=HTMLResponse)
async def deck_edit_component(deck_id: str, render = Depends(template('components/deck_home_show.html'))):
	return render()


@router.get("/edit/{deck_id}/confirm-delete", response_class=HTMLResponse)
async def deck_edit_component(deck_id: str, render = Depends(template('components/modal.html'))):
	return render(
		title=f"Deleting {deck_id}", 
		content=f"Are you <b>really sure</b> you wanna delete the deck named {deck_id}? It contains XXXX cards!"
	)
