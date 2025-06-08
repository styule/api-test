import time  # for rate limiting
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agenttest1.orchestrator import generate_post

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

app = FastAPI(title="Ask Steve: Multi-Agent AI Assistant")
templates = Jinja2Templates(directory="agenttest1/templates")

# --- RATE LIMITING CODE ---
RATE_LIMIT = {}
MAX_REQUESTS = 10
WINDOW = 60


@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    ip = request.client.host or "unknown"
    window = int(time.time() // WINDOW)
    key = f"{ip}-{window}"
    RATE_LIMIT.setdefault(key, 0)
    RATE_LIMIT[key] += 1
    if RATE_LIMIT[key] > MAX_REQUESTS:
        return PlainTextResponse("Too many requests", status_code=429)
    return await call_next(request)


# --- SECURITY HEADERS MIDDLEWARE ---
class SecureHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self' 'unsafe-inline';"
        )
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return response


app.add_middleware(SecureHeadersMiddleware)

# --- ROUTES ---


class PostRequest(BaseModel):
    topic: str


@app.post("/generate")
async def generate(request: PostRequest):
    post = await generate_post(request.topic)
    return {"post": post}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def index_post(request: Request, topic: str = Form(...)):
    post = await generate_post(topic)
    return templates.TemplateResponse(
        "index.html", {"request": request, "topic": topic, "post": post}
    )


@app.get("/health")
def health():
    return {"status": "ok"}
