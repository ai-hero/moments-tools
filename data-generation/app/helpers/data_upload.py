import sys
import logging
import os
from io import BytesIO
from minio import Minio

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


def upload(local_file: str, s3_path):
    with open(local_file, "rb") as file:
        value_as_a_stream = BytesIO(file.read())
        minio_client.put_object(
            DATA_BUCKET,
            s3_path,
            value_as_a_stream,
            value_as_a_stream.getbuffer().nbytes,
        )
