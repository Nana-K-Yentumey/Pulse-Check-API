from fastapi import FastAPI, HTTPException
from app.models import MonitorCreate, MonitorResponse, StatusResponse
from app.store import monitors
from app.watchdog import start_timer, cancel_timer

app = FastAPI(
    title="Pulse Check API",
    description="A Dead Man's Switch API for monitoring remote devices.",
)

@app.post("/monitor", response_model=MonitorResponse, status_code=201)
async def register_monitor(data: MonitorCreate):
    if data.id in monitors:
        raise HTTPException(status_code=409, detail=f"Monitor '{data.id}' already exists.")
    
    monitors[data.id] = {
        "id": data.id,
        "timeout": data.timeout,
        "alert_email": data.alert_email,
        "status": "active",
        "task": None
    }

    start_timer(data.id)

    return monitors[data.id]

@app.post("/monitors/{device_id}/heartbeat", response_model=StatusResponse)
async def heartbeat(device_id: str):
    if device_id not in monitors:
        raise HTTPException(status_code=404, detail=f"Monitor '{device_id}' not found.")
    
    monitor = monitors[device_id]

    cancel_timer(device_id)
    monitor["status"] = "active"
    start_timer(device_id)

    return StatusResponse(
        id=device_id,
        status="active",
        message=f"Hearbeat received. Timer reset to {monitor['timeout']} seconds."
    )

@app.post("/monitors/{device_id}/pause", response_model=StatusResponse)
async def pause_monitor(device_id: str):
    if device_id not in monitors:
        raise HTTPException(status_code=404, detail=f"Monitor '{device_id}' not found.")

    cancel_timer(device_id)
    monitor["status"] = "paused"

    return StatusResponse(
        id=device_id,
        status="paused",
        message=f"Monitor '{device_id}' paused. No alerts will fire."
    )

@app.get("/monitors/{device_id}", response_model=StatusResponse)
async def get_monitor(device_id: str):
    if device_id not in monitors:
        raise HTTPException(status_code=404, detail=f"Monitor '{device_id}' not found.")
    
    return monitors[device_id]

@app.get("/monitors", response_model=list[MonitorResponse])
async def list_monitors():
    return list(monitors.values())