from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.core import Base, engine
from entities.routers.user_router import user_router
from entities.routers.wish_router import wish_router
from auth.routes.auth_router import auth_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    
    print("Database created")
    
    yield
    
    print("Database closed")
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth_router, prefix='/api')
app.include_router(user_router, prefix='/api', tags=['Users'])
app.include_router(wish_router, prefix='/api', tags=['Wishes'])

@app.get("/health", tags=['Health Checks'])
def read_root():
    return {"health": "true"}