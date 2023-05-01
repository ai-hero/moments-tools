import openai
import sys
import logging
from moments.agent import Agent
from moments.moment import Moment, Self, Participant

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
        moment_with_init = Moment.parse(self.agent_config.config["init"])
        messages.append({"role": "system", "content": str(moment_with_init)})
        for occurrence in moment.occurrences:
            if isinstance(occurrence, Self):
                messages.append(
                    {"role": "assistant", "content": occurrence.content["says"]}
                )
            elif isinstance(occurrence, Participant):
                messages.append({"role": "user", "content": occurrence.content["says"]})

        # Complete with openai
        response = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=messages)
        response_message = response["choices"][0]["message"]
        line = response_message["content"].splitlines()[0].strip()
        print(f"-->{line}<--")
        import re

        if not re.match(r"^Self:\s+(\((.*)\)\s+)?\"(.+)\"$", line):
            # Try to fix it
            if not line.startswith('"'):
                line = '"' + line
            if not line.endswith('"'):
                line = line + '"'
            if not line.startswith("Self: "):
                line = "Self: " + line
        return Self.parse(line)
