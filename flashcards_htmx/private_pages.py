from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/home", response_class=HTMLResponse)
async def home_page(render = Depends(template('private/home.html'))):
	return render(navbar_title="Home")


@router.get("/study", response_class=HTMLResponse)
async def study_page(render = Depends(template('private/study.html'))):
	return render(navbar_title="Study")
		



@router.post("/logout", response_class=HTMLResponse)
async def logout_page(request: Request):
	return render()
	
