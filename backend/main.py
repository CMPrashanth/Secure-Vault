import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from db.session import init_db
from routes import auth, vault, admin

# --- App and Rate Limiter Setup ---
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Secure PII Service")

# --- ADDED FOR DEBUGGING ---
@app.get("/")
def read_root():
    return {"status": "backend_is_running"}
# --- END OF DEBUGGING CODE ---

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Database Initialization on Startup ---
@app.on_event("startup")
def on_startup():
    init_db()

# --- Production-Ready CORS Configuration ---
# We read the frontend's URL from an environment variable.
client_origin_url = os.getenv("CLIENT_ORIGIN_URL", "http://localhost:5173")

# The list of allowed origins for CORS requests.
origins = [
    client_origin_url,
]

# For convenience, we add localhost to the list if the main origin is a production URL,
# ensuring local development still works without changing environment variables.
if "localhost" not in client_origin_url:
    origins.extend(["http://localhost:5173", "http://127.0.0.1:5173"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Routers ---
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(vault.router, prefix="/api/vault", tags=["Vault"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])