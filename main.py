from fastapi import FastAPI
from router.index import router as model_router

app = FastAPI(title="Database Migration App")

app.include_router(model_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
