import typing

from pathlib import Path
from datetime import datetime
import importlib.metadata

from jinja2 import Environment, contextfunction
from jinja2.loaders import PackageLoader
from fastapi import Request, Depends
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


__version__ = importlib.metadata.version('flashcards_htmx')



# Create the FastAPI app
app = FastAPI(
    title="Flashcards HTMX webserver",
    description="API Docs for flashcards-htmx",
    version=__version__,
)
#templates = Jinja2Templates(directory=Path(__file__).parent / "templates" / "public")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")



def get_jinja2():
    """ Get Jinja2 dependency function. you can define more functions, filters or global vars here """
    @contextfunction
    def url_for(context: dict, name: str, **path_params: typing.Any) -> str:
        request = context["request"]
        return request.url_for(name, **path_params)

    env = Environment(loader=PackageLoader("flashcards_htmx"), autoescape=True)
    env.globals["url_for"] = url_for
    env.globals["this_year"] = lambda: datetime.utcnow().year

    return env


def template(tpl : str):
    """ Get view render function using Jinja2 environment injected above """
    def func_view(request: Request, env : Environment = Depends(get_jinja2)):
        template = env.get_template(tpl)
        def render(*args, **kwargs):
            return template.render(request=request, *args, **kwargs)
        return render
    return func_view



from flashcards_htmx.public_pages import router as public_router # noqa: F401, E402
from flashcards_htmx.private_pages import router as private_router # noqa: F401, E402
from flashcards_htmx.private_components import router as private_components # noqa: F401, E402

app.include_router(public_router)
app.include_router(private_router)
app.include_router(private_components)



