from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth.router import router as auth_router
from src.api.threads.router import router as threads_router
from src.api.posts.router import router as posts_router
from src.core.database import create_db

## TEST - for creating db
@asynccontextmanager
async def lifespan(current_app: FastAPI):
    print("Starting Forum")
    await create_db()

    yield

    print("Server shutting down")

app = FastAPI(
    title="Simple forum",
    description="Небольшой сервис для общения через треды и посты",
    version="1.0.0",

    lifespan=lifespan
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(threads_router)
app.include_router(posts_router)
