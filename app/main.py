from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ComtradeRequest
from app.comtrade_api import fetch_comtrade_data
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vercel frontend için
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/get-comtrade-data")
async def get_data(request: ComtradeRequest):
    try:
        data = fetch_comtrade_data(request)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))