import os
import requests
from dotenv import load_dotenv
from app.schemas import ComtradeRequest
import logging
logging.basicConfig(level=logging.INFO)
import comtradeapicall


load_dotenv()
API_KEY = os.getenv("PRIMARY_KEY")
import os
logging.info(f"🔑 Subscription Key log: {os.getenv('PRIMARY_KEY')[:6] if os.getenv('PRIMARY_KEY') else '❌ NOT SET'}")
print(f"🔑 Subscription Key (first 6 chars): {os.getenv('PRIMARY_KEY')[:6] if os.getenv('PRIMARY_KEY') else '❌ NOT SET'}")
def fetch_comtrade_data(req: ComtradeRequest):
    try:
        

        logging.info(f"🔑 Subscription Key (first 6 chars): {API_KEY[:6] if API_KEY else '❌ NOT SET'}")

        result = comtradeapicall.previewFinalData(
            typeCode='C',
            freqCode=req.freqCode,
            clCode='HS',
            period=req.period,
            reporterCode=','.join(req.reporterCode),
            cmdCode=req.cmdCode,
            flowCode=req.flowCode,
            partnerCode=','.join(req.partnerCode) if req.partnerCode else None,
            partner2Code=None,
            customsCode=None,
            motCode=None,
            maxRecords=5000,
            format_output='JSON',
            aggregateBy=None,
            breakdownMode='classic',
            countOnly=None,
            includeDesc=True
        )
        print(result)
        logging.info(f" result: {result}")
        simplified = [{
            "reporter": d.get("reporterDesc", ""),
            "partner": d.get("partnerDesc", ""),
              "product": d.get("cmdDescE", ""),
            "period": d.get("period", ""),
            "fobvalue": d.get("fobvalue", 0),
            "netWgt": d.get("netWgt", 0),
        } for d in result.to_dict('records')]

        return simplified

    except Exception as e:
        logging.error("Comtrade fetch error: %s", str(e))
        return []