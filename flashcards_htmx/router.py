from pathlib import Path

from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter(prefix="/home")


@router.get("/")
async def home(request: Request):
	return templates.TemplateResponse("public/landing-page.html", {"request":request})
	