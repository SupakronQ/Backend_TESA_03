from fastapi import APIRouter,Query
from ..models.hydrometrics import Dams,Stations
from ..config.db import conn
from ..schemas.tranform_data import serializeDict,serializeList
from bson import ObjectId
from datetime import datetime

hydrometrics = APIRouter()

# ---- GET METHOD ----

@hydrometrics.get('/')
async def find_all_data(name: str = Query(None, description="Name parameter, if provided, filters by name")):

    if name:
        # กรณีรับพารามิเตอร์ name ให้ query ข้อมูลที่มี name ตรงกัน
        return serializeList(conn.local.hydrometrics.find({"name": name}))
    else:
        # กรณีไม่ได้รับพารามิเตอร์ name ให้แสดงทั้งหมด
        return serializeList(conn.local.hydrometrics.find())

@hydrometrics.get('/source/')
async def get_all_source(source: str = Query(None, description="dam or station")):

    if source in ["dam","station"]:
        # กรณีรับพารามิเตอร์ name ให้ query ข้อมูลที่มี name ตรงกัน
        return list(conn.local.hydrometrics.distinct("name",{"type_source":f"{source}"}))
    else:
        # กรณีไม่ได้รับพารามิเตอร์ name ให้แสดงทั้งหมด
        return list(conn.local.hydrometrics.distinct("name"))

@hydrometrics.get('/{id}')
async def find_one_record(id):
    return serializeDict(conn.local.hydrometrics.find_one({"_id":ObjectId(id)}))

@hydrometrics.get("/hydrometrics/")
async def get_dams(
    start_time: datetime = Query(..., description="Start time of the range"),
    end_time: datetime = Query(..., description="End time of the range"),
    name: str = Query(..., description="Name of dam or station Example ")
):
    result = conn.local.hydrometrics.find({
    "timestamp": {
        "$gte": start_time,
        "$lte": end_time
    },
    "name":f"{name}"
})
    return serializeList(result)

# ---- POST METHOD ----

@hydrometrics.post('/dam')
async def create_dam_record(data: Dams):
    record = dict(data)
    conn.local.hydrometrics.insert_one(record)
    return serializeList(conn.local.hydrometrics.find({"type_source": "dam","name":f"{record['name']}"}))

@hydrometrics.post('/station')
async def create_station_record(data: Stations):
    record = dict(data)
    conn.local.hydrometrics.insert_one(record)
    return serializeList(conn.local.hydrometrics.find({"type_source": "station","name":f"{record['name']}"}))

# ---- PUT METHOD ----

@hydrometrics.put('/{id}')
async def update_record(id,data: Dams):
    conn.local.hydrometrics.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(data)})
    return serializeDict(conn.local.hydrometrics.find_one({"_id":ObjectId(id)}))

# ---- DELETE METHOD ----

@hydrometrics.delete('/{id}')
async def delete_record(id):
    return serializeDict(conn.local.hydrometrics.find_one_and_delete({"_id":ObjectId(id)}))



