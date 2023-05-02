import sys
import logging
import os
from copy import deepcopy
import httpx
from moments.agent import Agent

LOGGER_URL = os.environ.get("LOGGER_URL", "http://logger:8080")


logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


def stash_snapshot(snapshot: dict, agent: Agent):
    snapshot = deepcopy(snapshot)
    snapshot_id = snapshot["snapshot_id"]
    snapshot["__agent_info"] = {
        "id": agent.id,
        "name": agent.name,
        "config": deepcopy(agent.config.__dict__),
    }
    with httpx.Client(base_url=LOGGER_URL) as client:
        print(f"{LOGGER_URL}/v1/snapshots/{snapshot_id}")
        response = client.post(f"/v1/snapshots/{snapshot_id}", json=snapshot)
        if response.status_code >= 400:
            LOG.error(
                "Unable to log moment: %s / snapshot: %s",
                snapshot["moment_id"],
                snapshot["snapshot_id"],
            )
