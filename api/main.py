import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chart.routes import router as chart_router
from api.database import init_db
from api.log import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_db()
    yield

app = FastAPI(
    title="Ascendant API",
    description="RESTful API for Astro Calculations",
    version="0.0.1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chart_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Ascendant API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


def main():
    uvicorn.run(
        "api.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )

if __name__ == "__main__":
    main()
