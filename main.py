from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from dotenv import load_dotenv
import os
import comtradeapicall
from comtradeapicall import _getFinalDataAvailability

load_dotenv()
subscription_key = os.getenv('PRIMARY_KEY')

app = FastAPI()

# CORS sadece frontend'e izin veriyor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ffront-comtrade.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/final-data")
def get_final_data(
    typeCode: str,
    freqCode: str,
    clCode: str,
    period: str,
    reporterCode: str,
    cmdCode: str,
    flowCode: str,
    partnerCode: Optional[str] = None,
    partner2Code: Optional[str] = None,
    maxRecords: int = 2500
):
    availability = _getFinalDataAvailability(typeCode, freqCode, clCode, period, reporterCode)
    if availability is None or availability.empty:
        return {"error": "No data available for the given parameters1."}

    df = comtradeapicall.getFinalData(
        subscription_key, typeCode, freqCode, clCode, period,
        reporterCode, cmdCode, flowCode, partnerCode,
        partner2Code, None, None, maxRecords, 'JSON', None,
        'classic', None, True
    )
    return df.to_dict(orient="records")

@app.get("/tariffline-data")
def get_tariffline_data(
    typeCode: str,
    freqCode: str,
    clCode: str,
    period: str,
    reporterCode: str,
    cmdCode: str,
    flowCode: str,
    partnerCode: Optional[str] = None,
    partner2Code: Optional[str] = None,
    maxRecords: int = 2500
):
    availability = _getFinalDataAvailability(typeCode, freqCode, clCode, period, reporterCode)
    if availability is None or availability.empty:
        return {"error": "No data available for the given parameterss."}

    df = comtradeapicall.getTarifflineData(
        subscription_key, typeCode, freqCode, clCode, period,
        reporterCode, cmdCode, flowCode, partnerCode,
        partner2Code, None, None, maxRecords, 'JSON',
        None, True
    )
    return df.to_dict(orient="records")

@app.get("/availability")
def get_availability(
    typeCode: str = 'C',
    freqCode: str = 'A',
    clCode: str = 'HS',
    period: str = '2021',
    reporterCode: Optional[str] = None
):
    df = comtradeapicall.getFinalDataAvailability(
        subscription_key,
        typeCode=typeCode,
        freqCode=freqCode,
        clCode=clCode,
        period=period,
        reporterCode=reporterCode
    )
    return df.to_dict(orient="records")