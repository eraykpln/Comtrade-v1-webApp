from pydantic import BaseModel
from typing import List, Optional

class ComtradeRequest(BaseModel):
    reporterCode: List[str]
    partnerCode: Optional[List[str]] = None
    cmdCode: str
    period: str  # "202205" veya "2021"
    flowCode: str  # "M" veya "X"
    freqCode: str = "M"  # "A" (yıllık) veya "M" (aylık)