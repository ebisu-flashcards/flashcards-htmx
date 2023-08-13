from typing import *
import shelve

from pathlib import Path
from datetime import datetime
import importlib.metadata
from functools import partial
from textwrap import dedent
from hashlib import md5

from jinja2 import Environment, pass_context
from jinja2.loaders import PackageLoader
from fastapi import Request, Depends
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException, StarletteHTTPException


__version__ = importlib.metadata.version("flashcards_htmx")

'''
Data structure:

{
    "schemas": {
        "1": {
            "name": "Q/A with reverse",
            "description": "Simple schema with a question and an answer. Generates the reverse card as well.",
            ... see default schema ...
        }
    }
    "decks": {
        "0": {
            "name": "Deck 0",
            "description": "Description for deck 0",
            "algorithm": "Random",
            "cards_data": {
                "0": {
                    "schema": "Q/A"
                    "tags": ["tag 0"],
                    "question": "Question 0",
                    "answer": "Answer 0"
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
'''


database = "flashcards.db"
shelve.open = partial(shelve.open, writeback=True)

with shelve.open(database) as db:
    db.setdefault("decks", {})
    db.setdefault(
        "schemas",
        {
            md5("Simple Q/A".encode()).hexdigest(): {
                "name": "Simple Q/A",
                "description": "Simple schema with a question and an answer.",

                "form": dedent("""
                    <label for='question'>Question</label>
                    <input type='text' name='question' value='{{ question }}'>

                    <label for='answer'>Answer</label>
                    <input type='text' name='answer' value='{{ answer }}'>
                """),
                "preview": "{{ question }} -> {{ answer }}",
                "cards": {
                    "card": {
                        "question": "{{ question }}",
                        "answer": "{{ answer }}",
                    }
                }
            },
            md5("Q/A with reverse".encode()).hexdigest(): {
                "name": "Q/A with reverse",
                "description": "Simple schema with a question and an answer. Generates the reverse card as well.",
                "form": dedent("""
                    <label for='question'>Question:</label>
                    <input type='text' name='question' value='{{ question }}'>

                    <label for='answer'>Answer:</label>
                    <input type='text' name='answer'  value='{{ answer }}'>
                """),
                "preview": "{{ question }} <-> {{ answer }}",
                "cards": {
                    "direct": {
                        "question": "{{ question }}",
                        "answer": "{{ answer }}",
                    },
                    "reverse": {
                        "question": "{{ answer }}",
                        "answer": "{{ question }}",
                    }
                }
            }
        },
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


# Create the FastAPI app
app = FastAPI(
    title="Flashcards HTMX webserver",
    description="API Docs for flashcards-htmx",
    version=__version__,
)
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    template = get_jinja2().get_template("public/http_error.html")
    response = template.render(
        request=request, code=exc.status_code, message=exc.detail
    )
    return HTMLResponse(response, status_code=exc.status_code)


from flashcards_htmx.api.public import router as public_router  # noqa: F401, E402
from flashcards_htmx.api.private import router as private_router  # noqa: F401, E402
from flashcards_htmx.api.study import router as study_router  # noqa: F401, E402
from flashcards_htmx.api.decks import router as decks_router  # noqa: F401, E402
from flashcards_htmx.api.cards import router as cards_router  # noqa: F401, E402
from flashcards_htmx.api.schemas import router as schemas_router  # noqa: F401, E402

app.include_router(public_router)
app.include_router(private_router)
app.include_router(study_router)
app.include_router(decks_router)
app.include_router(cards_router)
app.include_router(schemas_router)
