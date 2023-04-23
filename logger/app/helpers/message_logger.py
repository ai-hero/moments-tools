import sys
import logging
import os
import json
from io import BytesIO
from minio import Minio
from threading import Thread

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


minio_client = Minio(
    os.environ["S3_URL"],
    access_key=os.environ["S3_ACCESS_KEY"],
    secret_key=os.environ["S3_SECRET_KEY"],
    region=os.environ["S3_REGION_NAME"],
    secure=(os.environ["S3_SECURE"] == "true"),
)
DATA_BUCKET = os.environ["DATA_BUCKET"]


def _save_to_file(
    bot_type: str,
    bot_id: str,
    bot_variant: str,
    conversation_id: str,
    message_id: str,
    message: dict,
):
    value = json.dumps(message)
    value_as_bytes = value.encode("utf-8")
    value_as_a_stream = BytesIO(value_as_bytes)
    minio_client.put_object(
        DATA_BUCKET,
        os.path.join(
            "llm-tool-data",
            bot_type,
            bot_id,
            bot_variant,
            conversation_id,
            message_id + ".json",
        ),
        value_as_a_stream,
        value_as_a_stream.getbuffer().nbytes,
    )


def save_to_file(
    bot_type: str,
    bot_id: str,
    bot_variant: str,
    conversation_id: str,
    message_id: str,
    message: dict,
):
    thread = Thread(
        target=_save_to_file,
        args=(bot_type, bot_id, bot_variant, conversation_id, message_id, message),
    )
    thread.start()
