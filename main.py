import logging
import time
import uuid
import secrets
from fastapi import FastAPI, Request
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

# --- Configuration des Logs ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Initialisation de l'app ---
app = FastAPI(title="DevOps Project API")
# TODO: Realiser des taches 
# --- Observabilité : Métriques ---
Instrumentator().instrument(app).expose(app)

# --- Base de données (Simulation) ---
quotes = [
    {"id": 1, "author": "Martin Fowler", "text": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."},
    {"id": 2, "author": "Gene Kim", "text": "Improving daily work is even more important than doing daily work."}
]

# --- Modèle de données ---
class Quote(BaseModel):
    author: str
    text: str

# --- Middleware : Tracing & Logging ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4()) # Génère un ID unique pour le tracing
    logger.info(f"START Request path={request.url.path} method={request.method} request_id={request_id}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time)
    # Ajoute l'ID de tracing dans les headers de réponse
    response.headers["X-Request-ID"] = request_id
    logger.info(f"END Request status={response.status_code} process_time={process_time:.4f}s request_id={request_id}")
    return response

# --- Routes de l'API ---
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API DevOps Quotes !"}

@app.get("/quotes")
def get_quotes():
    return quotes

@app.get("/quotes/random")
def get_random_quote():
    return secrets.choice(quotes)

@app.post("/quotes", status_code=201)
def create_quote(quote: Quote):
    new_id = len(quotes) + 1
    new_quote = {"id": new_id, "author": quote.author, "text": quote.text}
    quotes.append(new_quote)
    logger.info(f"Nouvelle citation ajoutée par {quote.author}")
    return new_quote