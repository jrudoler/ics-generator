# from transformers import AutoModelForCausalLM, AutoTokenizer
import outlines
from icalendar import Calendar, Event
from typing import Optional
import datetime
from schema import EventDetails
import os
import argparse
from prompts import event_details_prompt
# tried using small local model, but it was both slow and not accurate enough
# def load_model():
#     model_name = "meta-llama/Llama-3.2-1B"
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForCausalLM.from_pretrained(model_name)
#     return tokenizer, model


def create_ics_file(event_details: dict, filename: Optional[str] = None) -> None:
    event = Event()
    event.add("summary", event_details["title"])
    event.add("dtstart", datetime.datetime.fromisoformat(event_details["start"]))
    event.add("dtend", datetime.datetime.fromisoformat(event_details["end"]))
    event.add("location", event_details["location"])

    cal = Calendar()
    cal.add("prodid", "-//My Calendar//mxm.dk//")
    cal.add("version", "2.0")
    cal.add_component(event)

    if filename is None:
        filename = event_details["filename"]
    path = os.path.join(os.getcwd(), "data", filename)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(cal.to_ical())


def main():
    # New CLI argument parsing
    parser = argparse.ArgumentParser(
        description="Generate ICS files from event details."
    )
    parser.add_argument(
        "user_prompt", type=str, help="The prompt to extract event details from."
    )
    parser.add_argument(
        "--filename", type=str, help="Optional filename for the ICS file."
    )
    args = parser.parse_args()

    ## get current date and time
    now = datetime.datetime.now()
    print("Current date and time:", now)

    # Use the user prompt from CLI arguments
    user_prompt = args.user_prompt

    # model = outlines.models.transformers("meta-llama/Llama-3.2-3B")
    model = outlines.models.openai("gpt-4o-mini")

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
    create_ics_file(
        dict(structure), filename=args.filename
    )  # Pass filename if provided
    # open the file
    os.system(f"open {os.path.join(os.getcwd(), 'data', dict(structure)['filename'])}")
    # TODO: find a nice way to clean up the data directory


if __name__ == "__main__":
    main()
