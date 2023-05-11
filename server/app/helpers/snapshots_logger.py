import sys
import logging
import os
from copy import deepcopy
import httpx
from moments.snapshot import Snapshot
from moments.agent import Agent

LOGGER_URL = os.environ.get("LOGGER_URL", "http://logger:8080")


logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


def stash_snapshot(snapshot: Snapshot, agent: Agent):
    snapshot_dict = deepcopy(snapshot.to_dict())
    snapshot_id = snapshot_dict["id"]
    snapshot_dict["__agent_info"] = {
        "id": agent.id,
        "name": agent.name,
        "config": deepcopy(agent.config.__dict__),
    }
    try:
        with httpx.Client(base_url=LOGGER_URL) as client:
            print(f"{LOGGER_URL}/v1/snapshots/{snapshot_id}")
            response = client.post(f"/v1/snapshots/{snapshot_id}", json=snapshot_dict)
            if response.status_code >= 400:
                LOG.error(
                    "Unable to log moment: %s / snapshot: %s",
                    snapshot_dict["moment"]["id"],
                    snapshot_id,
                )
    except httpx.ConnectError as ce:
        LOG.error("Error loggiing - %s", str(ce))
    except Exception as ex:  # pylint: disable=broad-exception-caught
        LOG.error("Error loggiing - %s", str(ex))
