import sys
import logging
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from moments.agent import Agent
from moments.moment import Moment, Participant, Self

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)

chat = ChatOpenAI(temperature=0)


class ChatOpenAiAgent(Agent):
    def respond(self: "ChatOpenAiAgent", moment: Moment) -> Self:
        langchain_messages = []
        moment_with_init = Moment.parse(self.agent_config.config["init"])
        langchain_messages.append(SystemMessage(content=str(moment_with_init)))
        for occurrence in moment.occurrences:
            if isinstance(occurrence, Self):
                langchain_messages.append(AIMessage(content=occurrence.content["says"]))
            elif isinstance(occurrence, Participant):
                langchain_messages.append(
                    HumanMessage(content=occurrence.content["says"])
                )

        # Complete with langchain
        response = chat(langchain_messages)
        line = response.content.splitlines()[0].strip()
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
