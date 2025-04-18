from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.auth import login_instagram, get_client
from app.dm import start_campaign

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    success, msg = await login_instagram(username, password)
    if not success:
        return templates.TemplateResponse("index.html", {"request": request, "error": msg})
    return RedirectResponse(url="/dashboard", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "step": "dashboard"})


@app.post("/start-campaign")
async def start(
    target: str = Form(...),
    message: str = Form(...),
    mode: str = Form(...),
    limit: int = Form(...),
    delay: float = Form(...),
):
    client = get_client()
    result = await start_campaign(client, target, message, mode, limit, delay)
    return {"status": "started", "details": result}
