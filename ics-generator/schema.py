# schema.py

from pydantic import BaseModel, ConfigDict, FutureDatetime, Field


class EventDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")  # required for openai
    title: str = Field(description="The title of the event")
    start: str = Field(description="The start date and time of the event (ISO format)")
    end: str = Field(description="The end date and time of the event (ISO format)")
    location: str = Field(description="The location of the event")
    filename: str = Field(
        description="The filename for the event, with .ics extension (no spaces)"
    )
