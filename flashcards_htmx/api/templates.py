from pathlib import Path
import shelve

from jinja2 import Template
import starlette.status as status
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template, database


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/templates", response_class=HTMLResponse)
async def templates_page(
    request: Request, render=Depends(template("private/templates.html"))
):
    return render(
        navbar_title="Templates",
        searchable=True,
        new_item_endpoint=request.url_for("create_template_page"),
        new_item_text="New Template...",
    )


@router.get("/htmx/components/templates", response_class=HTMLResponse)
async def templates_component(render=Depends(template("responses/templates.html"))):
    with shelve.open(database) as db:
        return render(templates=db["templates"])


@router.get("/templates/new", response_class=HTMLResponse)
async def create_template_page(render=Depends(template("private/template.html"))):
    with shelve.open(database) as db:
        template_id = str(len(db["templates"]) + 1)
    return render(
        navbar_title="New Template",
        template_id=template_id,
        template={
            "name": "Q/A",
            "question": "{{ word }}",
            "answer": "{{ word }}",
            "preview": "{{ question }} -> {{ answer }}",
            "form": "<input type='text' name='question.word'><input type='text' name='answer.word'>",
        },
    )


@router.get("/templates/{template_id}", response_class=HTMLResponse)
async def edit_template_page(
    template_id: str, render=Depends(template("private/template.html"))
):
    with shelve.open(database) as db:
        template = db["templates"].get(template_id, {})
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
    return render(
        navbar_title=template_id,
        template_id=template_id,
        template=template,
    )


@router.post("/template/{template_id}", response_class=RedirectResponse)
async def save_template_endpoint(template_id: str, request: Request):
    async with request.form() as form:
        with shelve.open(database) as db:
            db["templates"][template_id] = {
                **db["templates"][template_id],
                "name": form["name"],
            }
    return RedirectResponse(
        request.url_for("templates_page"), status_code=status.HTTP_302_FOUND
    )


@router.get(
    "/htmx/components/template/{template_id}/confirm-delete", response_class=HTMLResponse
)
async def template_confirm_delete_component(
    template_id: str, render=Depends(template("components/message-modal.html"))
):
    with shelve.open(database) as db:
        deck = db["templates"].get(template_id, {})
        if not deck:
            raise HTTPException(status_code=404, detail="Template not found")

    return render(
        title=f"Deleting template",
        content=f"Are you really sure you wanna delete the template '{template_id}'?",
        positive=f"Yes, delete {template_id}",
        negative=f"No, don't delete",
        delete_endpoint="delete_template_endpoint",
        endpoint_params={"template_id": template_id},
    )


@router.get("/templates/{template_id}/delete", response_class=RedirectResponse)
async def delete_deck_endpoint(request: Request, template_id: str):
    with shelve.open(database) as db:
        if template_id not in db["templates"]:
            raise HTTPException(status_code=404, detail="Template not found")
        del db["templates"][template_id]

    return RedirectResponse(
        request.url_for("templates_page"), status_code=status.HTTP_302_FOUND
    )
