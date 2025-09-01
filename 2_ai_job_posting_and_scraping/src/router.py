from src.interactor.bot_controller import BotController

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()
controller = BotController()

# Adiciona suporte a CORS para qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/chat", methods=["GET", "POST"])
def chat(description: str = Body(..., embed=True)):

    result = controller.extract_job(description=description)

    if not result:
        return {"error": "Não foi possível criar o modelo de trabalho."}
    else:
        return {"job_model": result}

@app.api_route("/scraper", methods=["GET", "POST"])
def scraper():

    result = controller.scrape_jobs()
    
    if not result:
        return {"error": "Não foi possível criar o modelo de trabalho."}
    else:
        return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("router:app", host="0.0.0.0", port=port, reload=True)
