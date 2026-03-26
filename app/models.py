from pydantic import BaseModel

class MonitorCreate(BaseModel):
    id: str
    timeout: int
    alert_email: str

class MonitorResponse(BaseModel):
    id: str
    timeout: int
    alert_email: str
    status: str

class StatusResponse(BaseModel):
    id: str
    status: str
    message: str