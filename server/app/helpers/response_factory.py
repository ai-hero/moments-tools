import sys
import logging
from functools import cache
import helpers.chat.chatgpt as chatgpt
import helpers.chat.chatopenai as chatopenai
import helpers.chat.llmopenai as llmopenai
import helpers.chat.llmcohere as llmcohere
from helpers.bot_config import BotConfig
from copy import deepcopy
from datetime import datetime
from uuid import uuid4
from typing import Callable

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)

ALLOW_OVERRIDE = False


def get_bot_response(
    conversation_id: str,
    conversation: dict,
    config_override: dict = None,
):
    conversation["id"] = conversation_id
    conversation["message_id"] = str(uuid4())
    conversation["request_id"] = str(uuid4())
    conversation["timestamp"] = f"{datetime.now().isoformat()}"
    conversation.pop("response_id", None)
    conversation = deepcopy(conversation)

    bot_id = conversation["bot_id"]
    bot_type = conversation["bot_type"]
    bot_variant = conversation["bot_variant"]
    bot_config = load_bot_config(bot_type, bot_id, bot_variant)
    if not ALLOW_OVERRIDE:
        # Don't do this in production - will be injecting stuff
        LOG.warning(
            "ALLOW_OVERRIDE is True. This will allow client to override agent config. Use for development only."
        )
        if config_override:
            LOG.warning("CRITICAL: OVERRIDING CONFIG for")
            bot_config = BotConfig(config_override)

    get_response_func: Callable = None
    if bot_type == "chatgpt":
        get_response_func = chatgpt.get_response
    elif bot_type == "chatopenai":
        get_response_func = chatopenai.get_response
    elif bot_type == "llmopenai":
        get_response_func = llmopenai.get_response
    elif bot_type == "llmcohere":
        get_response_func = llmcohere.get_response

    if get_response_func:
        # Prepare messages including system message
        conversation["messages"] = [
            message
            for message in conversation.get("messages", [])
            if message["role"] in ["user", "assistant"]
        ]
        # Override system message with the updated instructions including context.
        system_message = {
            "role": "system",
            "content": bot_config.get_system_message(conversation.get("context", None)),
        }
        conversation["messages"].insert(0, system_message)
        response_message = get_response_func(bot_config, conversation)
        if response_message["content"].startswith(f"{bot_config.assistant}: "):
            response_message["content"] = response_message["content"][
                len(f"{bot_config.assistant}: ") :
            ]
        conversation["messages"].append(response_message)
        LOG.info(
            "%s/%s| %s: %s\t%s: %s",
            bot_config.config["type"],
            conversation["id"],
            bot_config.config["roles"].get(
                conversation["messages"][-2]["role"], "System"
            ),
            conversation["messages"][-2]["content"],
            bot_config.config["roles"].get(
                conversation["messages"][-1]["role"], "System"
            ),
            conversation["messages"][-1]["content"],
        )

    else:
        conversation["messages"].append(
            {
                "role": "assistant",
                "content": "Umm... I'm afraid I can't help as I am not sure what type of bot I am.",
            }
        )

    conversation["message_id"] = str(uuid4())
    conversation["timestamp"] = f"{datetime.now().isoformat()}"
    conversation["response_id"] = str(uuid4())
    return conversation


@cache
def load_bot_config(bot_type: str, bot_id: str, bot_variant: str):
    config_file = f"{bot_type}-{bot_id}-{bot_variant}.yaml"
    LOG.info("Loading bot config from file: %s", config_file)
    return BotConfig.from_file(config_file)
