import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from cors import add_cors

# Default Cloudflare-friendly settings
ENABLE_DOCS = os.getenv("documentation", "false").lower() == "true"
DOCS_URL = "/docs" if ENABLE_DOCS else None
REDOC_URL = "/redoc" if ENABLE_DOCS else None
ALLOW_NO_URL_PARAM = os.getenv("no_url_param", "false").lower() == "true"
ALLOWED_ORIGINS = os.getenv("origins", "*")  # Allow all by default for Cloudflare

app = FastAPI(openapi_url=None, docs_url=DOCS_URL, redoc_url=REDOC_URL)

if ENABLE_DOCS:
    @app.get('/')
    async def home(_: Request):
        return RedirectResponse(DOCS_URL)

# Cloudflare runs on port 8080 (force it)
PORT = 8080

# Add CORS middleware
add_cors(app, ALLOWED_ORIGINS, ALLOW_NO_URL_PARAM)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=PORT)
