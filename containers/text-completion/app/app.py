import traceback
import falcon
from falcon import Request, Response
from routes.health_check import HealthCheck
from routes.predict import Predict


def custom_handle_uncaught_exception(
    _: Request, resp: Response, exception: Exception, __: dict
):
    # 1. Print the stack trace in the logs so someone can debug.
    traceback.print_exc()

    # 2. Raise a 500 error so someone gets paged.
    resp.status = falcon.HTTP_500
    resp.media = f"{exception}"


app = falcon.App()
app.add_error_handler(Exception, custom_handle_uncaught_exception)

# The routes
app.add_route("/", HealthCheck())
app.add_route("/predict", Predict())

# Alternative routes (e.g. for Sagemaker)
app.add_route("/ping", HealthCheck())
app.add_route("/invocations", Predict())
