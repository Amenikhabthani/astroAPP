from fastapi import FastAPI
from api.endpoints import router as astrology_router

app = FastAPI(title="Astrology API")

# Include the router
app.include_router(astrology_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
