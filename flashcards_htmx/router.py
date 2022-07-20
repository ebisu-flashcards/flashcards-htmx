from pathlib import Path

from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/")
async def home(request: Request):
	return templates.TemplateResponse("public/landing-page.html", {"request":request})
	

@router.get("/login")
async def login(request: Request):
	return templates.TemplateResponse("public/login.html", {"request":request})
	

@router.get("/signup")
async def signup(request: Request):
	return templates.TemplateResponse("public/signup.html", {"request":request})


@router.get("/reset-password")
async def reset_password(request: Request):
	return templates.TemplateResponse("public/reset-password.html", {"request":request})
