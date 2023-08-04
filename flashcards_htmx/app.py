import typing
import shelve

from pathlib import Path
from datetime import datetime
import importlib.metadata

from jinja2 import Environment, pass_context
from jinja2.loaders import PackageLoader
from fastapi import Request, Depends
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


__version__ = importlib.metadata.version("flashcards_htmx")


# Create the FastAPI app
app = FastAPI(
    title="Flashcards HTMX webserver",
    description="API Docs for flashcards-htmx",
    version=__version__,
)
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

db = shelve.open("flashcards.db", writeback=True)
card_templates = db.get("templates", {
        "Q/A": {
            "question": "{{ word }}",
            "answer": "{{ word }}",
            "preview": "{{ question }} -> {{ answer }}"
        }})
decks = db.get("decks", {})
print(decks)


def get_jinja2():
    """Get Jinja2 dependency function. you can define more functions, filters or global vars here"""

    @pass_context
    def url_for(context: dict, name: str, **path_params: typing.Any) -> str:
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
