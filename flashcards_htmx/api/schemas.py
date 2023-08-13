from pathlib import Path
import shelve
from textwrap import dedent
from hashlib import md5

import starlette.status as status
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from flashcards_htmx.app import template, database


templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
router = APIRouter()


@router.get("/schemas", response_class=HTMLResponse)
async def schemas_page(
    request: Request, render=Depends(template("private/schemas.html"))
):
    return render(
        navbar_title="Schemas",
        searchable=True,
        new_item_endpoint=request.url_for("create_schema_page"),
        new_item_text="New Schema...",
    )


@router.get("/htmx/components/schemas", response_class=HTMLResponse)
async def schemas_component(render=Depends(template("responses/schemas.html"))):
    with shelve.open(database) as db:
        schemas = db["schemas"]
        for schema in schemas.values():
            schema["usage"] = 0

        # Get all the cards that uses this schema across all decks
        for deck in db["decks"].values():
            for card in deck["cards"].values():
                if card["schema"] in schemas:
                    schemas[card["schema"]]["usage"] += 1

        return render(schemas=schemas)


@router.get("/schemas/new", response_class=HTMLResponse)
async def create_schema_page(render=Depends(template("private/schema-code.html"))):
    with shelve.open(database) as db:
        schema_id = str(len(db["schemas"]) + 1)
    return render(
        navbar_title="New Schema",
        schema_id=schema_id,
        schema={
            "name": "New Schema",
            "description": "The schema's description.",
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


@router.get("/schemas/view/{schema_id}", response_class=HTMLResponse)
async def view_schema_page(
    schema_id: str, render=Depends(template("private/schema-readonly.html"))
):
    with shelve.open(database) as db:
        schema = dict(**db["schemas"].get(schema_id, {}))  # To avoid automatic creation of a new schema
        del schema["usage"]
        if not schema:
            raise HTTPException(status_code=404, detail="Schema not found")
    return render(
        navbar_title=schema["name"],
        schema_id=schema_id,
        schema=schema,
    )


@router.get("/schemas/new/{schema_id}", response_class=HTMLResponse)
async def clone_schema_page(
    schema_id: str, render=Depends(template("private/schema-code.html"))
):
    with shelve.open(database) as db:
        schema = dict(**db["schemas"].get(schema_id, {}))  # To avoid automatic creation of a new schema
        if not schema:
            raise HTTPException(status_code=404, detail="Schema not found")
        schema["name"] = f"Clone of {schema['name']}"
        del schema["usage"]
        schema_id = md5(schema["name"].encode()).hexdigest()
    return render(
        navbar_title=schema["name"],
        schema_id=schema_id,
        schema=schema,
    )


@router.post("/schema/new", response_class=RedirectResponse)
async def save_schema_endpoint(request: Request):
    async with request.form() as form:
        schema = eval(form["code"])
        schema_id = md5(schema["name"].encode()).hexdigest()
        with shelve.open(database) as db:
            if schema_id in db["schemas"]:
                raise HTTPException(
                    status_code=409, detail="Schema with this ID already exists"
                )
            db["schemas"][schema_id] = schema
    return RedirectResponse(
        request.url_for("schemas_page"), status_code=status.HTTP_302_FOUND
    )


@router.get(
    "/htmx/components/schema/{schema_id}/confirm-delete", response_class=HTMLResponse
)
async def schema_confirm_delete_component(
    schema_id: str, render=Depends(template("components/message-modal.html"))
):
    with shelve.open(database) as db:
        schema = db["schemas"].get(schema_id, {})
        if not schema:
            raise HTTPException(status_code=404, detail="Schema not found")

    return render(
        title=f"Deleting schema",
        content=f"Are you really sure you wanna delete the schema '{schema['name']}'?",
        positive=f"Yes, delete {schema['name']}",
        negative=f"No, don't delete",
        delete_endpoint="delete_schema_endpoint",
        endpoint_params={"schema_id": schema_id},
    )


@router.get("/schemas/{schema_id}/delete", response_class=RedirectResponse)
async def delete_schema_endpoint(request: Request, schema_id: str):
    with shelve.open(database) as db:
        if schema_id not in db["schemas"]:
            raise HTTPException(status_code=404, detail="Schema not found")
        del db["schemas"][schema_id]

    return RedirectResponse(
        request.url_for("schemas_page"), status_code=status.HTTP_302_FOUND
    )
