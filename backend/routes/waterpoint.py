from fastapi import APIRouter,Query
from models.waterpoint import Waterpoint
from config.db import conn
from schemas.waterpoint import serializeDict,serializeList
from bson import ObjectId
from datetime import datetime

waterpoint = APIRouter()

@waterpoint.get('/')
async def find_all_data():
    return serializeList(conn.local.waterpoint.find())

@waterpoint.get('/{id}')
async def find_one_record(id):
    return serializeDict(conn.local.waterpoint.find_one({"_id":ObjectId(id)}))

@waterpoint.get("/waterpoints/")
async def get_waterpoints(
    start_time: datetime = Query(..., description="Start time of the range"),
    end_time: datetime = Query(..., description="End time of the range")
):
    result = conn.local.waterpoint.find({
    "created": {
        "$gte": start_time,
        "$lte": end_time
    }
})
    return serializeList(result)

@waterpoint.post('/')
async def create_record(data: Waterpoint):
    conn.local.waterpoint.insert_one(dict(data))
    return serializeList(conn.local.waterpoint.find())

@waterpoint.put('/{id}')
async def update_record(id,data: Waterpoint):
    conn.local.waterpoint.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(data)})
    return serializeDict(conn.local.waterpoint.find_one({"_id":ObjectId(id)}))

@waterpoint.delete('/{id}')
async def delete_record(id):
    return serializeDict(conn.local.waterpoint.find_one_and_delete({"_id":ObjectId(id)}))