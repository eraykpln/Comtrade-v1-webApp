import requests
import pandas as pd

def getFinalData(subscription_key, **kwargs):
    url = "https://comtradeapi.un.org/public/v1/getFinalData"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.get(url, headers=headers, params=kwargs)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data["data"])