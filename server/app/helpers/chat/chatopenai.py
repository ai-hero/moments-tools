from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import sys
import logging
from helpers.bot_config import BotConfig

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)

chat = ChatOpenAI(temperature=0)


def get_response(bot_config: BotConfig, conversation: dict):
    messages: list[dict] = conversation["messages"]
    # Complete with langchain
    langchain_messages = []
    for message in messages:
        if message["role"] == "system":
            langchain_messages.append(SystemMessage(message["content"]))
        elif message["role"] == "user":
            langchain_messages.append(HumanMessage(message["content"]))
        elif message["role"] == "assistant":
            langchain_messages.append(AIMessage(message["content"]))
    response = chat(langchain_messages)
    response_message = {"role": "assistant", "content": response.content}
    return response_message
