from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from tts_service import TTSService

app = FastAPI()
tts_service = TTSService(audio_dir='app/static/audio_cache')

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_audio")
async def generate_audio(request: Request):
    data = await request.json()
    text = data.get("text")
    lang = data.get("lang", "en")  # Default to English if no language is specified
    if not text:
        return JSONResponse(content={"error": "No text provided"}, status_code=400)
    audio_path = tts_service.get_audio(text, lang)
    relative_path = '/static/audio_cache/' + os.path.basename(audio_path)
    return JSONResponse(content={"audio_path": relative_path})

if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run(app, host="0.0.0.0", port=8093)