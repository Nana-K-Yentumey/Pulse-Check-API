import asyncio
import logging
from datetime import datetime

from app.store import monitors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def trigger_alert(device_id: str):
    await asyncio.sleep(monitors[device_id]["timeout"])

    if device_id not in monitors:
        return
    
    monitor = monitors[device_id]

    if monitor["status"] != "active":
        return
    
    monitor["status"] = "down"

    alert = {
        "ALERT": f"Device {device_id} is down!",
        "time": datetime.utcnow().isoformat(),
        "alert_email": monitor["alert_email"]
    }

    logger.critical(alert)

    def start_timer(device_id: str):
        loop = asyncio.get_event_loop()
        task = loop.create_task(trigger_alert(device_id))
        monitors[device_id]["task"] = task

def cancel_timer(device_id: str):
    monitor = monitors.get(device_id)
    if monitor and monitor.get("task"):
        monitor["task"].cancel()
        monitor["task"] = None

    