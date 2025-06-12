import os
import requests
from dotenv import load_dotenv
from app.schemas import ComtradeRequest
import logging
logging.basicConfig(level=logging.INFO)


load_dotenv()
API_KEY = os.getenv("PRIMARY_KEY")
import os
logging.info(f"🔑 Subscription Key log: {os.getenv('PRIMARY_KEY')[:6] if os.getenv('PRIMARY_KEY') else '❌ NOT SET'}")
print(f"🔑 Subscription Key (first 6 chars): {os.getenv('PRIMARY_KEY')[:6] if os.getenv('PRIMARY_KEY') else '❌ NOT SET'}")
def fetch_comtrade_data(req: ComtradeRequest):
    try:
        base_url = "https://comtradeapi.un.org/public/v1/getFinalData"
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

        logging.info(f"🌍 Base URL: {base_url}")
        logging.info(f"🔧 Headers: {headers}")
        logging.info(f"🧾 Params: {params}")
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        logging.info("Status Code: %s", response.status_code)
        logging.info("Response Body: %s", response.text)

        if "dataset" not in data or not isinstance(data["dataset"], list):
            logging.warning("No dataset found in response.")
            return []

        simplified = [{
            "reporter": d.get("reporterDesc", ""),
            "partner": d.get("partnerDesc", ""),
            "product": d.get("cmdDescE", ""),
            "period": d.get("period", ""),
            "fobvalue": d.get("fobvalue", 0),
            "netWgt": d.get("netWgt", 0),
        } for d in data["dataset"]]

        return simplified

    except Exception as e:
        logging.error("Comtrade fetch error: %s", str(e))
        return []