import sys
import logging
import os
import json
import csv
from io import BytesIO
from minio import Minio
from threading import Thread
from tempfile import NamedTemporaryFile
from urllib3.response import HTTPResponse
from collections import defaultdict
from helpers.bot_config import BotConfig

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
            "llm-tool-conversations",
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


def create_dataset(bot_type: str, bot_id: str, bot_variant: str):
    prefix = os.path.join("llm-tool-conversations", bot_type, bot_id, bot_variant)
    LOG.info("Listing all objects for conversation - %s.", prefix)
    objects = minio_client.list_objects(
        DATA_BUCKET,
        prefix=prefix,
        recursive=True,
    )
    conversations = defaultdict(list)
    for o in objects:
        if o.object_name[len(prefix) :]:
            try:
                response: HTTPResponse = minio_client.get_object(
                    DATA_BUCKET, o.object_name
                )
                message = json.loads(response.read().decode("utf-8"))
                conversation_id = message["id"]
                conversations[conversation_id].append(message)
            finally:
                response.close()
                response.release_conn()
    bot_config = BotConfig.from_file("dataset_generator.yaml")
    LOG.info("Loaded the generator bot config.")
    dataset = []
    for conversation_id, messages in conversations.items():
        all_messages = {}
        all_message_ids = []
        all_parent_ids = []
        for message in messages:
            if "message_id" in message and "previous_message_id" in message:
                all_messages[message["message_id"]] = message
                all_message_ids.append(message["message_id"])
                if message["previous_message_id"]:
                    all_parent_ids.append(message["previous_message_id"])
        leaf_messages = [item for item in all_message_ids if item not in all_parent_ids]
        LOG.info(
            "%s leaf-messages found in the conversation %s",
            len(leaf_messages),
            conversation_id,
        )
        for message_id in leaf_messages:
            message = all_messages[message_id]
            # This will return entire conversation.
            conv = bot_config.build_entire_conversation(message)
            # Uncomment to see the constructed text.
            # print(conv)
            dataset.append(
                {
                    "conversation_id": message["id"],
                    "message_id": message["message_id"],
                    "conversation": conv,
                }
            )
    with NamedTemporaryFile(suffix=".csv") as ntf:
        LOG.info("Building training dataset file.")
        with open(ntf.name, "w", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["conversation_id", "message_id", "conversation"],
                delimiter=",",
                quotechar='"',
            )
            writer.writeheader()
            writer.writerows(dataset)

        LOG.info("Uploading training dataset file.")
        dataset_file = os.path.join(
            "llm-tool-dataset",
            bot_config.config["type"],
            bot_config.config["id"],
            bot_config.config["variant"],
            f"from-{bot_type}-{bot_id}-{bot_variant}.csv",
        )
        with open(ntf.name, "rb") as file:
            value_as_a_stream = BytesIO(file.read())
            minio_client.put_object(
                DATA_BUCKET,
                dataset_file,
                value_as_a_stream,
                value_as_a_stream.getbuffer().nbytes,
            )
        LOG.info("Done.")
        LOG.info("File uploaded to %s", dataset_file)
