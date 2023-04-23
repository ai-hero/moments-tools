import os
from langchain.llms import Cohere
import sys
import logging
from pprint import pformat
from helpers.bot_config import BotConfig

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


COHERE_API_KEY = os.environ["COHERE_API_KEY"]
llm = Cohere(cohere_api_key=COHERE_API_KEY)


def get_response(bot_config: BotConfig, conversation: dict):
    # Complete with langchain
    prompt = bot_config.build_prompt(conversation)
    response = llm(prompt)
    response_message = {
        "role": "assistant",
        "content": response.splitlines()[0].strip(),
    }
    return response_message
