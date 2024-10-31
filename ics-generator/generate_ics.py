from transformers import AutoModelForCausalLM, AutoTokenizer
import outlines
from icalendar import Calendar, Event
from typing import List, AnyStr
import datetime
from pydantic import BaseModel
from schema import EventDetails


def load_model():
    model_name = "meta-llama/Llama-3.2-1B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model


# def extract_event_details(text: str, tokenizer, model) -> dict:
#     inputs = tokenizer(text, return_tensors="pt")
#     with torch.no_grad():
#         output = model.generate(**inputs, max_length=100)

#     structured_output = tokenizer.decode(output[0], skip_special_tokens=True)
#     # Parsing of structured_output into event details should be done here


#     return {
#         "title": "Meeting with Alex",  # Example extraction
#         "start": "2024-11-05 14:00:00",
#         "end": "2024-11-05 15:00:00",
#         "location": "Office",
#     }


def create_ics_file(event_details: dict, filename: str = "event.ics") -> None:
    event = Event(
        summary=event_details["title"],
        dtstart=event_details["start"],
        dtend=event_details["end"],
        location=event_details["location"],
    )
    cal = Calendar()
    cal.add_component(event)

    with open(filename, "wb") as f:
        f.write(cal.to_ical())


@outlines.prompt
def event_details_prompt(
    user_prompt: str, now: datetime.datetime, response_schema: BaseModel
):
    """
    You are a helpful assistant that extracts event details from a prompt.
    The current date and time is {{ now }}. You must use this date and time to
    help determine the start and end times of the event, as the event has to be
    scheduled in the future.
    The user's prompt is: {{ user_prompt }}

    Return a valid JSON string with the following specification:
    {{ response_schema | schema }}
    """


def main():
    ## get current date and time
    now = datetime.datetime.now()
    print("Current date and time:", now)
    # get user input
    user_prompt = input("Enter your prompt: ")

    model = outlines.models.transformers("meta-llama/Llama-3.2-1B", device="mps")
    # model = outlines.models.openai("gpt-4o-mini")

    prompt = event_details_prompt(user_prompt, now, EventDetails)

    # tokenizer, model = load_model()
    # structure = extract_event_details(prompt, tokenizer, model)
    generator = outlines.generate.json(
        model,
        EventDetails,
        # system="You are a helpful assistant that extracts event details from a prompt.",
    )
    structure = generator(prompt)
    print(dict(structure))
    create_ics_file(dict(structure))


if __name__ == "__main__":
    main()
