from pydantic import BaseModel
from datetime import datetime
import pytz

class Waterpoint(BaseModel):
    point1: float
    point2: float
    created: datetime = datetime.now(pytz.timezone('Asia/Bangkok'))