import falcon
import sys
import logging
from helpers.message_logger import save_to_file

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


class MessageLogger:
    def on_get(
        self,
        _: falcon.Request,
        resp: falcon.Response,
        message_id: str,
    ) -> falcon.Response:
        """Handles prediction requests as GET"""
        LOG.info("GET Message: %s", message_id)
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = {}
        return resp

    # @jsonschema.validate(REQUEST_SCHEMA)
    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        message_id: str,
    ) -> falcon.Response:
        """Handles prediction requests as POST"""
        message = req.get_media()
        LOG.info("POST Message: %s", message_id)

        save_to_file(
            bot_type=message["bot_type"],
            bot_id=message["bot_id"],
            bot_variant=message["bot_variant"],
            conversation_id=message["id"],
            message_id=message["message_id"],
            message=message,
        )

        # Response body
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = {"status": "ok"}
        return resp
