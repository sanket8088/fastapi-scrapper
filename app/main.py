from fastapi import FastAPI
from app.routers import scrape

app = FastAPI()

app.include_router(scrape.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
