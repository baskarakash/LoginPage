from fastapi import FastAPI
from app.routes import auth
from app.dependencies import get_database
from app.models import create_tables

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Additional logging setup for uvicorn
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)

if __name__ == "__main__":
    # Create tables in the database
    create_tables()

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
