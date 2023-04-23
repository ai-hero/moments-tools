import sys
import logging
import os
from copy import deepcopy
import httpx
from helpers.bot_config import BotConfig

LOGGER_URL = os.environ.get("LOGGER_URL", "http://chat-logger:8080")


logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


def stash_chat_message(conversation, bot_config: BotConfig = None):
    message = deepcopy(conversation)
    message_id = conversation["message_id"]
    if bot_config:
        message["bot_config"] = bot_config.config
    with httpx.Client(base_url=LOGGER_URL) as client:
        print(f"{LOGGER_URL}/v1/messages/{message_id}")
        response = client.post(f"/v1/messages/{message_id}", json=message)
        if response.status_code >= 400:
            LOG.error(
                "Unable to log conversation: %s / message: %s",
                conversation["id"],
                message_id,
            )
