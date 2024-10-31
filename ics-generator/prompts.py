import outlines
import datetime
from pydantic import BaseModel


@outlines.prompt
def event_details_prompt(
    user_prompt: str, now: datetime.datetime, response_schema: BaseModel
):
    """
    You are a helpful assistant that extracts event details from a prompt.
    The current date and time is {{ now }}. You must use this date and time to
    help determine the start and end times of the event, as the event has to be
    scheduled in the future.
    You must return the start and end times in ISO format. Typically it is
    fair to assume that a standard "meeting" lasts 1 hour unless otherwise
    specified, but other types of events may have different durations and
    you should use your best judgement.
    The user's prompt is: {{ user_prompt }}

    Return a valid JSON string with the following specification (dates in ISO format
    and filenames with .ics extension and no spaces):
    {{ response_schema | schema }}
    """
