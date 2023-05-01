import sys
import logging
import pathlib
from functools import cache
from copy import deepcopy
from datetime import datetime
from uuid import uuid4
import pytz
from moments.agent import AgentConfig, AgentFactory, Agent
from moments.moment import Moment, Self, Participant, Context


logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)

ALLOW_OVERRIDE = False

DEFAULT_AGENT_INFO = {
    "kind": "ChatGptAgent",
    "id": "cafe",
    "variant": "01",
}


def get_agent(agent_instance_id: str, agent_config_override: dict) -> Agent:
    if not ALLOW_OVERRIDE:
        # Don't do this in production - will be injecting stuff
        LOG.warning(
            "ALLOW_OVERRIDE is True. This will allow client to override agent config. Use for development only."
        )
        agent_config_override.pop("apiVersion", None)
        if agent_config_override:
            agent_config = AgentConfig(**agent_config_override)
            LOG.warning(
                "CRITICAL: OVERRIDING CONFIG for moment: %s - %s-%s-%s ",
                agent_instance_id,
                agent_config.kind,
                agent_config.id,
                agent_config.variant,
            )
    if not agent_config:
        agent_config = load_agent_config(
            DEFAULT_AGENT_INFO["kind"],
            DEFAULT_AGENT_INFO["id"],
            DEFAULT_AGENT_INFO["variant"],
        )

    # Imports are dynamic, as keys might not be set in .env file for
    # the rest. Load and register the classes.
    match agent_config.kind:
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

    # Fetch Agent Instance
    return AgentFactory.create(agent_instance_id, agent_config)


def get_next_snapshot(
    agent_instance_id: str,
    moment_id: str,
    snapshot: dict,
    agent_config_override: dict = None,
):
    agent = get_agent(agent_instance_id, agent_config_override)
    assert agent

    snapshot_id = str(uuid4())
    assert "previous_snapshot_id" in snapshot
    snapshot["timestamp"] = datetime.now().isoformat()

    assert "occurrences" in snapshot

    LOG.debug(moment_id)
    # stash_chat_message(moment=moment)
    snapshot = deepcopy(snapshot)

    moment = Moment.parse("")
    for occurrence in snapshot["occurrences"]:
        kind = occurrence.pop("kind", None)
        match kind:
            case "Self":
                moment.occurrences.append(Self(**occurrence))
            case "Participant":
                moment.occurrences.append(Participant(**occurrence))
            case "Context":
                moment.occurrences.append(Context(**occurrence))
        occurrence["kind"] = kind  # Put it back

    if not moment.occurrences or (
        moment.occurrences and not isinstance(moment.occurrences[0], Context)
    ):
        tz = pytz.timezone("America/Los_Angeles")
        current_time = datetime.now(tz)
        moment.occurrences.insert(
            0, Context('```{"time": "' + current_time.strftime("%I:%M %p") + '"}```')
        )

    self_response = agent.respond(moment)
    snapshot["occurrences"].append(
        {"kind": "Self", "emotion": "", "says": self_response.content["says"]}
    )
    snapshot["previous_snapshot_id"] = snapshot_id  # Chain it
    snapshot["snapshot_id"] = str(uuid4())
    snapshot["timestamp"] = datetime.now().isoformat()
    # stash_chat_message(moment=moment, bot_config=bot_config)
    return snapshot


@cache
def load_agent_config(agent_kind: str, agent_id: str, agent_variant: str):
    config_file = (
        pathlib.Path(__file__).parent.resolve()
        / "configs"
        / f"{agent_kind}-{agent_id}-{agent_variant}.yaml"
    )
    LOG.info("Loading bot config from file: %s", config_file)
    return AgentConfig.from_file(config_file)
