import starlette.status as status
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from flashcards_htmx.app import template


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def landing_page(render=Depends(template("public/landing-page.html"))):
    return render()


@router.get("/login", response_class=HTMLResponse)
async def login_page(render=Depends(template("public/login.html"))):
    return render()


@router.post("/login", response_class=RedirectResponse)
async def login_action(request: Request):
    # FIXME Actually do the login!
    return RedirectResponse(
        request.url_for("home_page"), status_code=status.HTTP_302_FOUND
    )


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(render=Depends(template("public/signup.html"))):
    return render()


@router.post("/signup", response_class=RedirectResponse)
async def signup_action(request: Request):
    # FIXME Actually do the signup!
    return RedirectResponse(
        request.url_for("home_page"), status_code=status.HTTP_302_FOUND
    )


@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(render=Depends(template("public/reset-password.html"))):
    return render()


@router.post("/reset-password", response_class=RedirectResponse)
async def reset_password_action(request: Request):
    # FIXME Actually do the password reset!
    return RedirectResponse(
        request.url_for("home_page"), status_code=status.HTTP_302_FOUND
    )
