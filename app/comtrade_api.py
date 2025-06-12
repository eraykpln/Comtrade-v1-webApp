import os
import requests
from dotenv import load_dotenv
from app.schemas import ComtradeRequest

load_dotenv()
API_KEY = os.getenv("PRIMARY_KEY")

def fetch_comtrade_data(req: ComtradeRequest):
    base_url = "https://comtradeapi.un.org/public/v1/get"
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY
    }

    params = {
        "typeCode": "C",
        "freqCode": req.freqCode,
        "clCode": "HS",
        "reporterCode": ",".join(req.reporterCode),
        "partnerCode": ",".join(req.partnerCode) if req.partnerCode else "",
        "cmdCode": req.cmdCode,
        "period": req.period,
        "flowCode": req.flowCode,
        "breakdownMode": "classic",
        "includeDesc": "true",
        "format": "json",
        "maxRecords": 5000
    }

    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    
    # JSON'dan sadece gerekli alanları çıkaralım
    simplified = [{
        "reporter": d["reporterDesc"],
        "partner": d.get("partnerDesc"),
        "product": d["cmdDescE"],
        "period": d["period"],
        "fobvalue": d["fobvalue"],
        "netWgt": d["netWgt"],
    } for d in data.get("dataset", [])]

    return simplified