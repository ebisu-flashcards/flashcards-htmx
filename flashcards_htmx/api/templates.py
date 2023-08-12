from pathlib import Path
import shelve
from textwrap import dedent

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
        templates = db["templates"]
        for template in templates.values():
            template["usage"] = 0

        # Get all the cards that uses this template across all decks
        for deck in db["decks"].values():
            for card in deck["cards"].values():
                if card["template"]["id"] in templates:
                    templates[card["template"]["id"]]["usage"] += 1

        return render(templates=templates)


@router.get("/templates/new", response_class=HTMLResponse)
async def create_template_page(render=Depends(template("private/template.html"))):
    with shelve.open(database) as db:
        template_id = str(len(db["templates"]) + 1)
    return render(
        navbar_title="New Template",
        template_id=template_id,
        template={
            "name": "New Template",
            "description": "The template's description.",
            "form": dedent("""
                <label for='question'>Question</label>
                <input type='text' name='question' value={{ question }}>

                <label for='answer'>Answer</label>
                <input type='text' name='answer'  value={{ answer }}>
            """),
            "cards": {
                "card": {
                    "sides": {
                        "Question": "{{ question }}",
                        "Answer": "{{ answer }}",
                    },
                    "preview": "{{ question }} -> {{ answer }}",
                    "flip_order": "['Question', 'Answer']",
                },
            }
        }
    )


@router.get("/templates/view/{template_id}", response_class=HTMLResponse)
async def view_template_page(
    template_id: str, render=Depends(template("private/template-readonly.html"))
):
    with shelve.open(database) as db:
        template = dict(**db["templates"].get(template_id, {}))  # To avoid automatic creation of a new template
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
    return render(
        navbar_title=template["name"],
        template_id=template_id,
        template=template,
    )


@router.get("/templates/new/{template_id}", response_class=HTMLResponse)
async def clone_template_page(
    template_id: str, render=Depends(template("private/template.html"))
):
    with shelve.open(database) as db:
        template = dict(**db["templates"].get(template_id, {}))  # To avoid automatic creation of a new template
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        template["name"] = f"Clone of {template['name']}"
        template_id = str(hash(template["name"]))
    return render(
        navbar_title=template["name"],
        template_id=template_id,
        template=template,
    )


@router.post("/template/new", response_class=RedirectResponse)
async def save_template_endpoint(request: Request):
    async with request.form() as form:
        template_id = str(hash(form["name"]))

        with shelve.open(database) as db:
            if template_id in db["templates"]:
                raise HTTPException(
                    status_code=409, detail="Template with this ID already exists"
                )

            template = {
                "name": form["name"],
                "description": form["description"],
                "form": form["form"],
            }
            if "cards" not in template:
                template["cards"] = {}

            for key, value in form.items():
                if key.startswith("cards__"):
                    card_name, key = key.split("__", maxsplit=2)[1:]
                    if card_name not in template["cards"]:
                        template["cards"][card_name] = {
                            "sides": {},
                            "preview": "",
                            "flip_order": [],
                        }
                    if key.startswith("sides"):
                        _, side_name = key.split("__", maxsplit=1)
                        template["cards"][card_name]["sides"][side_name] = value

            db["templates"][template_id] = template
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
        template = db["templates"].get(template_id, {})
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")

    return render(
        title=f"Deleting template",
        content=f"Are you really sure you wanna delete the template '{template['name']}'?",
        positive=f"Yes, delete {template['name']}",
        negative=f"No, don't delete",
        delete_endpoint="delete_template_endpoint",
        endpoint_params={"template_id": template_id},
    )


@router.get("/templates/{template_id}/delete", response_class=RedirectResponse)
async def delete_template_endpoint(request: Request, template_id: str):
    with shelve.open(database) as db:
        if template_id not in db["templates"]:
            raise HTTPException(status_code=404, detail="Template not found")
        del db["templates"][template_id]

    return RedirectResponse(
        request.url_for("templates_page"), status_code=status.HTTP_302_FOUND
    )
