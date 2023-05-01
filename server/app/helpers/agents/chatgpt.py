import re
import sys
import logging
import openai
from moments.agent import Agent
from moments.moment import Moment, Self, Participant, Context

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


OPENAI_MODEL = "gpt-3.5-turbo"
assert OPENAI_MODEL in [model["id"] for model in openai.Model.list()["data"]]
openai.ChatCompletion.create(
    model=OPENAI_MODEL, messages=[{"role": "system", "content": "Say hi"}]
)


class ChatGptAgent(Agent):
    def respond(self: "ChatGptAgent", moment: Moment) -> Self:
        messages = []
        moment_with_init = Moment.parse(self.config.init)
        messages.append({"role": "system", "content": str(moment_with_init)})
        for occurrence in moment.occurrences:
            if isinstance(occurrence, Context):
                messages[0]["content"] += str(occurrence) + "\n"
            elif isinstance(occurrence, Self):
                messages.append(
                    {"role": "assistant", "content": occurrence.content["says"]}
                )
            elif isinstance(occurrence, Participant):
                messages.append({"role": "user", "content": occurrence.content["says"]})

        # Complete with openai
        print(f"{messages}")
        response = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=messages)
        response_message = response["choices"][0]["message"]
        line = response_message["content"].splitlines()[0].strip()
        print(f"-->{line}<--")
        if not re.match(r"^Self:\s+(\((.*)\)\s+)?\"(.+)\"$", line):
            # Try to fix it
            if not line.startswith('"'):
                line = '"' + line
            if not line.endswith('"'):
                line = line + '"'
            if not line.startswith("Self: "):
                line = "Self: " + line
        return Self.parse(line)
