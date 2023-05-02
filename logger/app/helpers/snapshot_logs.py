import sys
import logging
import os
import json
import csv
from io import BytesIO
from minio import Minio
from tempfile import NamedTemporaryFile
from urllib3.response import HTTPResponse
from collections import defaultdict
from moments.moment import Moment

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


def save_to_file(
    agent_kind: str,
    agent_id: str,
    agent_variant: str,
    agent_instance_id: str,
    moment_id: str,
    snapshot_id: str,
    snapshot: dict,
):
    print(
        agent_kind,
        agent_id,
        agent_variant,
        agent_instance_id,
        moment_id,
        snapshot_id + ".json",
    )
    value = json.dumps(snapshot)
    value_as_bytes = value.encode("utf-8")
    value_as_a_stream = BytesIO(value_as_bytes)
    minio_client.put_object(
        DATA_BUCKET,
        os.path.join(
            "moments",
            "snapshots",
            agent_kind,
            agent_id,
            agent_variant,
            agent_instance_id,
            moment_id,
            snapshot_id + ".json",
        ),
        value_as_a_stream,
        value_as_a_stream.getbuffer().nbytes,
    )


def create_dataset(agent_kind: str, agent_id: str, agent_variant: str):
    prefix = os.path.join("moments", "snapshots", agent_kind, agent_id, agent_variant)
    LOG.info("Listing all 'leaf' snapshots for all agent instances of - %s.", (prefix))
    objects = minio_client.list_objects(
        DATA_BUCKET,
        prefix=prefix,
        recursive=True,
    )
    moments = defaultdict(list)
    for o in objects:
        if o.object_name[len(prefix) :]:
            try:
                response: HTTPResponse = minio_client.get_object(
                    DATA_BUCKET, o.object_name
                )
                snapshot = json.loads(response.read().decode("utf-8"))
                moment_id = snapshot["moment_id"]
                moments[moment_id].append(snapshot)
            finally:
                response.close()
                response.release_conn()

    output_snapshots = []
    dataset = []
    for moment_id, snapshots in moments.items():
        all_snapshots = {}
        all_snapshot_ids = []
        all_parent_ids = []
        for snapshot in snapshots:
            if "snapshot_id" in snapshot and "previous_snapshot_id" in snapshot:
                all_snapshots[snapshot["snapshot_id"]] = snapshot
                all_snapshot_ids.append(snapshot["snapshot_id"])
                if snapshot["previous_snapshot_id"]:
                    all_parent_ids.append(snapshot["previous_snapshot_id"])

        leaf_snapshots = [
            all_snapshots[snapshot_id]
            for snapshot_id in all_snapshot_ids
            if snapshot_id not in all_parent_ids
        ]
        LOG.info(
            "%s leaf-snapshots found in the moment %s",
            len(leaf_snapshots),
            moment_id,
        )
        output_snapshots.extend(leaf_snapshots)

    LOG.info("Loaded the generator bot config.")
    for snapshot in leaf_snapshots:
        # This will return entire conversation.
        moment = Moment.parse(snapshot)
        agent_info = snapshot["__agent_info"]
        # Save to S3 in a new thread because it's slow

        # Uncomment to see the constructed text.
        print(str(moment))
        dataset.append(
            {
                "agent_kind": agent_info["config"]["kind"],
                "agent_id": agent_info["config"]["id"],
                "agent_variant": agent_info["config"]["variant"],
                "agent_instance_id": agent_info["id"],
                "moment_id": snapshot["moment_id"],
                "snapshot_id": snapshot["snapshot_id"],
                "moment": str(moment),
            }
        )

    with NamedTemporaryFile(suffix=".csv") as ntf:
        LOG.info("Building training dataset file.")
        with open(ntf.name, "w", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "agent_kind",
                    "agent_id",
                    "agent_variant",
                    "agent_instance_id",
                    "moment_id",
                    "snapshot_id",
                    "moment",
                ],
                delimiter=",",
                quotechar='"',
            )
            writer.writeheader()
            writer.writerows(dataset)

        LOG.info("Uploading training dataset file.")
        dataset_file = os.path.join(
            "datasets",
            f"from-{agent_kind}-{agent_id}-{agent_variant}.csv",
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
