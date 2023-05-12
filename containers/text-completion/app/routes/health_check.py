import falcon
from helpers.zero_shot_text_classification import ZeroShotTextClassifier

# Load the model on import
ZeroShotTextClassifier.load()


class HealthCheck:
    def on_get(self, _: falcon.Request, resp: falcon.Response) -> falcon.Response:
        """Warm-up the model before container becomes healthy."""
        # We load the model
        ZeroShotTextClassifier.load()

        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = {"status": "ok"}
        return resp
