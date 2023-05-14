import re
import sys
import logging
from falcon import HTTPError
import httpx
from moments.agent import Agent
from moments.moment import Moment, Self, Context, Rejected

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)

MODEL_URL = "http://text-completion:8080"


class TextCompletionAgent(Agent):
    def before(self: "TextCompletionAgent", moment: Moment):
        pass

    def do(self: "TextCompletionAgent", moment: Moment):
        # Add final "Self:" for agent to speak.
        prompt = str(moment) + "Self: "
        print(f"-->{prompt}<--")
        if prompt == "Self: ":
            moment.occurrences.append(
                Self.parse(
                    'Self: "Hi, How can I help? You can ask me any questions about personal finance."'
                )
            )
            return

        # prompt = prompt.replace("Self: ", "Assistant: ")
        # prompt = re.sub(r"User\s\(\d+\)\s:", "Human:", prompt)

        # Complete with fine tunded model
        try:
            with httpx.Client(base_url=MODEL_URL) as client:
                request = {"prompt": prompt}
                response = client.post(f"{MODEL_URL}/predict", json=request, timeout=20)
                if response.status_code >= 400:
                    LOG.error("Unable to get a prediction")
                    raise HTTPError(501, "It's not you it's me.")
                print(request, response.json())
        except httpx.ConnectError as ce:
            raise HTTPError(502, "It's not you it's me.")
        line = (
            response.json()["completion"][0]["generated_text"][len(prompt) :]
            .split("\n")[0]
            .strip()
        )
        print(f"-->{line}<--")
        if not re.match(r"^Self:\s+(\((.*)\)\s+)?\"(.+)\"$", line):
            # Try to fix it
            if not line.startswith('"'):
                line = '"' + line
            if not line.endswith('"'):
                line = line + '"'
            if not line.startswith("Self: "):
                line = "Self: " + line

        # Get the rejected
        try:
            with httpx.Client(base_url=MODEL_URL) as client:
                response = client.post(f"{MODEL_URL}/predict", json=request)
                if response.status_code >= 400:
                    LOG.error("Unable to get a prediction")
                    raise HTTPError(501, "It's not you it's me.")
                print(request, response.json())
        except httpx.ConnectError as ce:
            raise HTTPError(502, "It's not you it's me.")
        rejected_line = (
            response.json()["completion"][0]["generated_text"][len(prompt) :]
            .split("\n")[0]
            .strip()
        )
        rejected_line = rejected_line.replace("Self: ", "Rejected: ")
        if not re.match(r"^Self:\s+(\((.*)\)\s+)?\"(.+)\"$", rejected_line):
            # Try to fix it
            if not rejected_line.startswith('"'):
                rejected_line = '"' + rejected_line
            if not rejected_line.endswith('"'):
                rejected_line = rejected_line + '"'
            if not rejected_line.startswith("Rejected: "):
                rejected_line = "Rejected: " + rejected_line

        # First, add the rejected
        print(f"-->{rejected_line}<--")
        moment.occurrences.append(Rejected.parse(rejected_line))
        # Then the actual response
        moment.occurrences.append(Self.parse(line))

    def after(self: "TextCompletionAgent", moment: Moment):
        pass
