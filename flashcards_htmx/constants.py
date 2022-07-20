import os

#: The domain name where this app is deployed
DOMAIN = os.environ.get("FLASHCARDS_DOMAIN", "localhost")

#: API server address
API_SERVER = os.environ.get("FLASHCARDS_API_SERVER", "localhost:8001")
