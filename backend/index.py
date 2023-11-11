from fastapi import FastAPI
from routes.waterpoint import waterpoint
from config.embedmqtt import client

app = FastAPI()
app.include_router(waterpoint)
 
 # ทำการเชื่อมต่อ MQTT broker
client.loop_start()


# หยุด loop ของ MQTT client เมื่อ FastAPI หยุดทำงาน
@app.on_event("shutdown")
async def on_shutdown():
    client.loop_stop()