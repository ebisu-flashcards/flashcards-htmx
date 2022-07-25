from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter(prefix="/_components")


@router.get("/decks", response_class=HTMLResponse)
async def decks_component(render = Depends(template('responses/decks.html'))):
	return render(decks=range(4))
	