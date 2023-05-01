import sys
import logging
import pathlib
from functools import cache
from copy import deepcopy
from datetime import datetime
from uuid import uuid4
from moments.agent import AgentConfig, AgentFactory
from moments.moment import Moment, Self, Participant


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
    request_message_id = conversation["message_id"]
    conversation["request_id"] = str(uuid4())
    conversation["timestamp"] = f"{datetime.now().isoformat()}"
    conversation.pop("response_id", None)

    agent_config = None
    if not ALLOW_OVERRIDE:
        # Don't do this in production - will be injecting stuff
        LOG.warning(
            "ALLOW_OVERRIDE is True. This will allow client to override agent config. Use for development only."
        )
        if config_override:
            agent_config = AgentConfig(config_override)
            LOG.warning(
                "CRITICAL: OVERRIDING CONFIG for conversation: %s - %s-%s-%s called %s",
                conversation_id,
                agent_config.config["kind"],
                agent_config.config["id"],
                agent_config.config["variant"],
                agent_config.config["name"],
            )
    if not agent_config:
        agent_config = load_agent_config(
            conversation["agent_kind"],
            conversation["agent_id"],
            conversation["agent_variant"],
        )

    # Load and register the classes to avoid api key errors
    match agent_config.config["kind"]:
        case "ChatGptAgent":
            from helpers.agents.chatgpt import ChatGptAgent

            AgentFactory.register(ChatGptAgent)
        case "ChatOpenAiAgent":
            from helpers.agents.chatopenai import ChatOpenAiAgent

            AgentFactory.register(ChatOpenAiAgent)
        case "LlmCohereAgent":
            from helpers.agents.llmcohere import LlmCohereAgent

            AgentFactory.register(LlmCohereAgent)
        case "LlmOpenAiAgent":
            from helpers.agents.llmopenai import LlmOpenAiAgent

            AgentFactory.register(LlmOpenAiAgent)

    if "messages" not in conversation:
        conversation["messages"] = []
    conversation["agent_type"] = agent_config.config["kind"]
    conversation["agent_id"] = agent_config.config["id"]
    conversation["agent_variant"] = agent_config.config["variant"]

    # stash_chat_message(conversation=conversation)
    conversation = deepcopy(conversation)

    # Depending on the agent_kind import the right response function.
    # Imports are dynamic, as keys might not be set in .env file for
    # the rest.
    agent = AgentFactory.create(agent_config)
    if agent:
        moment = Moment.parse("")
        for message in conversation["messages"]:
            if message["role"] == "assistant":
                moment.occurrences.append(Self(emotion="", says=message["content"]))
            elif message["role"] == "user":
                moment.occurrences.append(
                    Participant(
                        name="User",
                        identifier="unidentified",
                        emotion="",
                        says=message["content"],
                    )
                )
        agent_response = agent.respond(moment)
        conversation["messages"].append(
            {"role": "assistant", "content": agent_response.content["says"]}
        )
    else:
        conversation["messages"].append(
            {
                "role": "assistant",
                "content": "Umm... I'm afraid I can't help as I am not sure what type of bot I am.",
            }
        )

    conversation["message_id"] = str(uuid4())
    conversation["previous_message_id"] = request_message_id  # Chain it
    conversation["timestamp"] = f"{datetime.now().isoformat()}"
    conversation["response_id"] = str(uuid4())
    # stash_chat_message(conversation=conversation, bot_config=bot_config)
    return conversation


@cache
def load_agent_config(agent_kind: str, agent_id: str, agent_variant: str):
    config_file = (
        pathlib.Path(__file__).parent.resolve()
        / "configs"
        / f"{agent_kind}-{agent_id}-{agent_variant}.yaml"
    )
    LOG.info("Loading bot config from file: %s", config_file)
    return AgentConfig.from_file(config_file)
