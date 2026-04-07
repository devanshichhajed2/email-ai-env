from pydantic import BaseModel
from typing import Optional

class Observation(BaseModel):
    email_text: str
    sender_type: str
    urgency: str
    emotion: str


class Action(BaseModel):
    category: Optional[str] = None
    reply: Optional[str] = None


class Reward(BaseModel):
    score: float
    feedback: str
    