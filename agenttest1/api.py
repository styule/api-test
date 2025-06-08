from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agenttest1.orchestrator import generate_post

app = FastAPI(title="Multi-Agent Blog Generator")
templates = Jinja2Templates(directory="agenttest1/templates")


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
