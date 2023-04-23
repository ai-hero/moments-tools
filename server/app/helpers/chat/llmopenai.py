from langchain.llms import OpenAI
import sys
import logging
from pprint import pformat
from helpers.bot_config import BotConfig

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)

llm = OpenAI(model_name="text-davinci-003", n=2, best_of=2)


def get_response(bot_config: BotConfig, conversation: dict):
    # Complete with langchain
    prompt = bot_config.build_prompt(conversation)
    response = llm(prompt)
    response_message = {"role": "assistant", "content": response.strip()}
    return response_message
