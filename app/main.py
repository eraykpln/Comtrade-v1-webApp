import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
import comtradeapicall
import pandas as pd

load_dotenv()
subscription_key = os.getenv("PRIMARY_KEY")

if not subscription_key:
    raise ValueError("❌ PRIMARY_KEY .env dosyasında tanımlı değil.")

app = FastAPI()

class ComtradeRequest(BaseModel):
    typeCode: str
    freqCode: str
    clCode: str
    period: str
    reporterCode: str
    cmdCode: str
    flowCode: str
    partnerCode: str | None = None
    partner2Code: str | None = None
    customsCode: str | None = None
    motCode: str | None = None
    maxRecords: int = 2500
    format_output: str = "JSON"
    aggregateBy: str | None = None
    breakdownMode: str = "classic"
    countOnly: bool | None = None
    includeDesc: bool = True

@app.post("/api/comtrade/final")
async def get_comtrade_final_data(req: ComtradeRequest):
    try:
        df = comtradeapicall.getFinalData(
            subscription_key=subscription_key,
            typeCode=req.typeCode,
            freqCode=req.freqCode,
            clCode=req.clCode,
            period=req.period,
            reporterCode=req.reporterCode,
            cmdCode=req.cmdCode,
            flowCode=req.flowCode,
            partnerCode=req.partnerCode,
            partner2Code=req.partner2Code,
            customsCode=req.customsCode,
            motCode=req.motCode,
            maxRecords=req.maxRecords,
            format_output=req.format_output,
            aggregateBy=req.aggregateBy,
            breakdownMode=req.breakdownMode,
            countOnly=req.countOnly,
            includeDesc=req.includeDesc
        )
        return df.head(100).to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}