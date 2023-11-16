from fastapi import FastAPI
from .routes.hydrometrics import hydrometrics
from .config.connectmqtt import client

 # ทำการเชื่อมต่อ MQTT broker
client.start()

app = FastAPI()
# app.include_router(waterpoint)
app.include_router(hydrometrics)

# หยุด loop ของ MQTT client เมื่อ FastAPI หยุดทำงาน
@app.on_event("shutdown")
async def on_shutdown():
    client.stop()