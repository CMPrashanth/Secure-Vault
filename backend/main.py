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
# --- MODIFICATION: Add redirect_slashes=True ---
app = FastAPI(title="Secure PII Service", redirect_slashes=True)
# --- END MODIFICATION ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Database and Router Initialization on Startup ---
@app.on_event("startup")
def on_startup():
    # Initialize the database
    init_db()
    # Include the API routers
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(vault.router, prefix="/api/vault", tags=["Vault"])
    app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

# --- Production-Ready CORS Configuration ---
client_origin_url = os.getenv("CLIENT_ORIGIN_URL", "http://localhost:5173")
origins = [
    client_origin_url,
    "https://secure-vault-eight-theta.vercel.app"
]
if "localhost" not in client_origin_url:
    origins.extend(["http://localhost:5173", "http://127.0.0.1:5173"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)