import os
from langchain.llms import OpenAI
import sys
import logging
from moments.agent import Agent
from moments.moment import Moment, Participant, Self, Instructions, Example

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)

llm = OpenAI(model_name="text-davinci-003", n=2, best_of=2)


class LlmOpenAiAgent(Agent):
    def respond(self: "LlmOpenAiAgent", moment: Moment) -> Self:
        moment_with_init = Moment.parse(self.agent_config.config["init"])
        for occurrence in moment.occurrences:
            if isinstance(occurrence, Self) or isinstance(occurrence, Participant):
                moment_with_init.occurrences.append(occurrence)

        # Add final "Self:" for agent to speak.
        prompt = str(moment_with_init) + "Self: "
        # Complete with langchain
        response = llm(prompt.strip())
        line = response.split("\n")[0].strip()
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
