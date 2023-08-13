from pathlib import Path
import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/settings", response_class=HTMLResponse)
async def profile_page(render=Depends(template("private/profile.html"))):
    return render(navbar_title="Settings")


@router.post("/logout", response_class=RedirectResponse)
async def logout_page(request: Request):
    return RedirectResponse(
        request.url_for("home_page"), status_code=status.HTTP_302_FOUND
    )
