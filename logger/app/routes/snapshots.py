import falcon
import sys
import logging
from threading import Thread
from helpers.snapshot_logs import save_to_file

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


class SnapshotLogger:
    # @jsonschema.validate(REQUEST_SCHEMA)
    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        snapshot_id: str,
    ) -> falcon.Response:
        """Handles logging requests as POST"""
        snapshot = req.get_media()
        assert snapshot["id"] == snapshot_id

        LOG.info("POST Snapshot: %s", str(snapshot_id))

        agent_info = snapshot["__agent_info"]
        # Save to S3 in a new thread because it's slow
        Thread(
            target=save_to_file,
            args=(
                agent_info["config"]["kind"],
                agent_info["config"]["id"],
                agent_info["config"]["variant"],
                agent_info["id"],
                snapshot["moment"]["id"],
                snapshot["id"],
                snapshot,
            ),
        ).start()

        # Response body
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = {"status": "ok"}
        return resp
