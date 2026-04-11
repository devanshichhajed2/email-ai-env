<<<<<<< HEAD
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
=======
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
>>>>>>> 9442762521da75db7afedec0a183407fecae9595
    