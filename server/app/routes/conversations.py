import falcon
import pytz
import sys
import logging
from helpers.response_factory import get_bot_response
from datetime import datetime

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


class Conversation:
    def on_get(
        self,
        _: falcon.Request,
        resp: falcon.Response,
        conversation_id: str,
    ) -> falcon.Response:
        """Handles prediction requests as GET"""
        LOG.info("GET Conversation: %s", conversation_id)
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = {}
        return resp

    # @jsonschema.validate(REQUEST_SCHEMA)
    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        conversation_id: str,
    ) -> falcon.Response:
        """Handles prediction requests as POST"""
        conversation = req.get_media()
        LOG.info("POST Conversation: %s", conversation_id)

        # Get bot from config
        config_override = conversation.get("config_override", None)

        # Inject context
        tz = pytz.timezone("America/New_York")
        current_time = datetime.now(tz)
        context = f"The time is {current_time.strftime('%I:%M %p')}"
        conversation["context"] = context
        conversation["timestamp"] = f"{datetime.now().isoformat()}"

        # Get response
        conversation = get_bot_response(conversation_id, conversation, config_override)

        # Response body
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = conversation
        return resp
