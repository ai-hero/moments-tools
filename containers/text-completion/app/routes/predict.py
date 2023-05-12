import falcon
from falcon.media.validators import jsonschema
from helpers.text_completion import Generator


REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {"type": "string", "minLength": 1, "maxLength": 1000},
    },
    "required": ["text"],
}


class Predict:
    @jsonschema.validate(REQUEST_SCHEMA)
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> falcon.Response:
        """Handles prediction requests as POST"""
        request_obj = req.get_media()
        prompt = request_obj["prompt"]
        completion = Generator.predict(prompt=prompt)
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = {"completion": completion}
        return resp
