from pydantic import BaseModel
from typing import Optional

class MonitorCreate(BaseModel):
    id: str
    timeout: int
    alert_email: str

class MonitorResponte(BaseModel):
    id: str
    timeout: int
    alert_email: str
    status: str

class StatusResponse(BaseModel):
    id: str
    status: str
    message: str