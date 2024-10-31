# schema.py

from pydantic import BaseModel, ConfigDict, FutureDatetime


class EventDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")  # required for openai
    title: str
    start: FutureDatetime
    end: FutureDatetime
    location: str = None
