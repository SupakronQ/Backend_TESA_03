from pydantic import BaseModel
from datetime import datetime
import pytz

class Source(BaseModel):
    type_source: str
    name: str
    water_level: float
    timestamp: datetime = datetime.now(pytz.timezone('Asia/Bangkok'))

    @staticmethod
    def default_type_source() -> str:
        return "source"

class Dams(Source):
    water_volume: float
    release_rate: float

    @staticmethod
    def default_type_source() -> str:
        return "dam"

class Stations(Source):
    flow_rate: float

    @staticmethod
    def default_type_source() -> str:
        return "station"
