from typing import *
import shelve

from pathlib import Path
from datetime import datetime
import importlib.metadata
from functools import partial

from jinja2 import Environment, pass_context
from jinja2.loaders import PackageLoader
from fastapi import Request, Depends
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


__version__ = importlib.metadata.version("flashcards_htmx")

"""
Data structure:

{
    "templates": {
        "Q/A": {
            "question": "{{ word }}"
            "answer": "{{ word }}"
            "preview": "{{ question }} -> {{ answer }}"
            "form": "<input type='text' name='question.word'><input type='text' name='answer.word'>"
        }
    }
    "decks": {
        "0": {
            "name": "Deck 0",
            "description": "Description for deck 0",
            "algorithm": "Random",
            "cards": {
                "0": {
                    "type": "Q/A",
                    "tags": ["tag 0"],
                    "data": {
                        "question": {
                            "word": "Question 0",
                            "example": "Example 0",
                        },
                        "answer": {
                            "word": "Answer 0",
                            "context": "Some context"
                        },
                        "preview": {
                            "divider": " -> ",
                        }
                    },
                    "reviews: {
                        "0": { 
                            "date": "2021-01-01",
                            "result: "Correct"
                        }
                    }
                },
                "1": { ... }
            }   
        },
        "1": { ... }
    }
}
"""

database = "flashcards.db"
shelve.open = partial(shelve.open, writeback=True)

with shelve.open(database) as db:
    db.setdefault("decks", {})
    db.setdefault("templates", {
        "Q/A": {
            "question": "{{ word }}",
            "answer": "{{ word }}",
            "preview": "{{ question.word }} -> {{ answer.word }}",
            "form": """
                <label for='question'>Question</label>
                <input type='text' name='question.word' value={{ question.word }}>

                <label for='answer'>Answer</label>
                <input type='text' name='answer.word'  value={{ answer.word }}>
            """
        }
    })


# Create the FastAPI app
app = FastAPI(
    title="Flashcards HTMX webserver",
    description="API Docs for flashcards-htmx",
    version=__version__,
)
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)


def get_jinja2():
    """Get Jinja2 dependency function. you can define more functions, filters or global vars here"""

    @pass_context
    def url_for(context: dict, name: str, **path_params: Any) -> str:
        request = context["request"]
        return request.url_for(name, **path_params)

    env = Environment(loader=PackageLoader("flashcards_htmx"), autoescape=True)
    env.globals["url_for"] = url_for
    env.globals["this_year"] = datetime.utcnow().year

    return env


def template(tpl: str):
    """Get view render function using Jinja2 environment injected above"""

    def func_view(request: Request, env: Environment = Depends(get_jinja2)):
        template = env.get_template(tpl)

        def render(*args, **kwargs):
            return template.render(request=request, *args, **kwargs)

        return render

    return func_view


from flashcards_htmx.api.public import router as public_router  # noqa: F401, E402
from flashcards_htmx.api.private import router as private_router  # noqa: F401, E402
from flashcards_htmx.api.components import (
    router as private_components,
)  # noqa: F401, E402

app.include_router(public_router)
app.include_router(private_router)
app.include_router(private_components)
