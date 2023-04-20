import falcon
from helpers.conversations_factory import get_bot


class Conversation:
    def on_get(
        self,
        _: falcon.Request,
        resp: falcon.Response,
        conversation_id: str,
    ) -> falcon.Response:
        """Handles prediction requests as GET"""
        print("GET:" + conversation_id)
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
        print("Post:" + conversation_id)
        bot_id = conversation["bot_id"]
        bot_type = conversation["bot_type"]
        bot = get_bot(bot_id, bot_type)
        conversation = bot.get_response(conversation)
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = conversation
        return resp
