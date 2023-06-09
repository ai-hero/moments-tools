import falcon
import sys
import logging
from helpers.moment_factory import system

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


class MomentsRoute:
    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        agent_instance_id: str,
    ) -> falcon.Response:
        """Handles prediction requests as POST"""
        obj = req.get_media()

        # Get agent config override from episode.
        # Keep it in so that it will be sent back in the response.
        agent_config_override = obj.pop("__agent_config_override", None)

        # Get response
        snapshot = system(agent_instance_id, agent_config_override)

        snapshot["__agent_config_override"] = agent_config_override

        # Response body
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = snapshot
        return resp
