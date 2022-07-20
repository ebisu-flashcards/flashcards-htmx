from pathlib import Path
import importlib.metadata

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


__version__ = importlib.metadata.version('flashcards_htmx')


# Create the FastAPI app
app = FastAPI(
    title="Flashcards HTMX webserver",
    description="API Docs for flashcards-htmx",
    version=__version__,
)


app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


from flashcards_htmx.router import router  # noqa: F401, E402
app.include_router(router)

# from flashcards_htmx.api.algorithms import (  # noqa: F401, E402
#     router as algorithms_router,
# )
# from flashcards_htmx.api.cards import router as cards_router  # noqa: F401, E402
# from flashcards_htmx.api.decks import router as decks_router  # noqa: F401, E402
# from flashcards_htmx.api.facts import router as facts_router  # noqa: F401, E402
# from flashcards_htmx.api.tags import router as tags_router  # noqa: F401, E402
# from flashcards_htmx.api.study import router as study_router  # noqa: F401, E402

# app.include_router(algorithms_router)
# app.include_router(cards_router)
# app.include_router(decks_router)
# app.include_router(facts_router)
# app.include_router(tags_router)
# app.include_router(study_router)

