import falcon
from helpers.text_completion import Generator

# Load the model on import
Generator.load()


class HealthCheck:
    def on_get(self, _: falcon.Request, resp: falcon.Response) -> falcon.Response:
        """Warm-up the model before container becomes healthy."""
        # We load the model
        Generator.load()

        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = {"status": "ok"}
        return resp
