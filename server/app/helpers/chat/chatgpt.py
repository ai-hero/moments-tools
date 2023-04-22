import openai
import sys
import logging
from pprint import pformat
from helpers.bot_config import BotConfig

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


OPENAI_MODEL = "gpt-3.5-turbo"
assert OPENAI_MODEL in [model["id"] for model in openai.Model.list()["data"]]
openai.ChatCompletion.create(
    model=OPENAI_MODEL, messages=[{"role": "system", "content": "Say hi"}]
)


def get_response(bot_config: BotConfig, conversation: dict):
    messages: list[dict] = conversation["messages"]
    # Complete with openai
    response = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=messages)
    response_message = response["choices"][0]["message"]
    return response_message
