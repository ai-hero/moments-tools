import os
import csv
import logging
import sys
import tarfile
from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile
from typing import Generator
from helpers.data_upload import upload
from moments.agent import AgentConfig
from moments.moment import Moment

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)


class DataGenerator(ABC):
    dataset_name: str
    dataset_path: str

    def __init__(self: "DataGenerator", dataset_name: str, dataset_path: str):
        self.dataset_name = dataset_name
        self.dataset_path = dataset_path

    @abstractmethod
    def build_data(self: "DataGenerator") -> Generator[Moment, None, None]:
        """Return a data generator that can yield moments"""


class DataFactory:
    @staticmethod
    def generate_data(data_generator: DataGenerator, agent_config: AgentConfig):
        init_moment = str(Moment.parse(agent_config.init))

        with NamedTemporaryFile(suffix=".csv") as ntf:
            LOG.info("Building training dataset file.")
            with open(ntf.name, "w", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "conversation",
                    ],
                    delimiter=",",
                    quotechar='"',
                )
                writer.writeheader()
                count = 0
                for moment in data_generator.build_data():
                    if count % 1000 == 0:
                        LOG.info("%s conversations generated", count)
                    conversation = f"{init_moment}\n{str(moment)}<|ENDOFTEXT|>"
                    writer.writerow({"conversation": conversation})
                    count += 1

            LOG.info("Compressing training dataset file.")
            with NamedTemporaryFile(suffix=".tar.gz") as ntfc:
                tar = tarfile.open(ntfc.name, "w:gz")
                tar.add(ntf.name)
                tar.close()

                LOG.info("Uploading training dataset file.")
                dataset_file = os.path.join(
                    "generated-datasets",
                    f"from-{data_generator.dataset_name}.csv.tar.gz",
                )
                upload(ntfc.name, dataset_file)
