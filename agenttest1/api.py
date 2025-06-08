import time  # <-- add this for rate limiting
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agenttest1.orchestrator import generate_post

app = FastAPI(title="Multi-Agent Blog Generator")
templates = Jinja2Templates(directory="agenttest1/templates")

# --- BEGIN RATE LIMITING CODE ---
RATE_LIMIT = {}  # Store per-IP counters in-memory
MAX_REQUESTS = 10  # Each IP allowed this many requests...
WINDOW = 60  # ...per this many seconds (here, 60 = 1 minute)


@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    ip = request.client.host or "unknown"
    window = int(time.time() // WINDOW)  # Current window bucket (e.g., "minute")
    key = f"{ip}-{window}"
    RATE_LIMIT.setdefault(key, 0)
    RATE_LIMIT[key] += 1
    if RATE_LIMIT[key] > MAX_REQUESTS:
        return PlainTextResponse("Too many requests", status_code=429)
    return await call_next(request)


# --- END RATE LIMITING CODE ---


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
