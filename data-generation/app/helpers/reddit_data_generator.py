import json
import logging
import sys
from collections import defaultdict
from pathlib import Path
from typing import Generator
from uuid import uuid4
from helpers.data_factory import DataGenerator
from moments.moment import Moment, Occurrence, Self, Participant
from tqdm import tqdm

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s | %(message)s"
)
LOG = logging.getLogger(__name__)

MAX_LINES_TOREAD = -1


class RedditDataGenerator(DataGenerator):
    def build_data(self: "DataGenerator") -> Generator[Moment, None, None]:
        """Return a data generator that can yield moments"""
        # LOG.info(
        #     "Loading all conversation topics from %s/conversations.json",
        #     self.dataset_path,
        # )
        # conversations: dict = {}
        # with open(
        #     Path(self.dataset_path) / "conversations.json", "r", encoding="utf"
        # ) as f:
        #     cs = json.loads(f.read())
        #     for cid, c in cs.items():
        #         conversations[cid] = c["title"]
        # LOG.info(
        #     "Found %s conversations in dataset %s.",
        #     len(conversations),
        #     self.dataset_name,
        # )

        LOG.info(
            "Loading all conversation topics from %s/utterances.jsonl",
            self.dataset_path,
        )
        LOG.info("First we count the number of lines.")
        total = 0
        with open(
            Path(self.dataset_path) / "utterances.jsonl", "r", encoding="utf"
        ) as f:
            for _ in f:
                if MAX_LINES_TOREAD > 0 and total > MAX_LINES_TOREAD:
                    break
                total += 1

        LOG.info("There are a total of %s utterances.", total)
        utterances: dict = defaultdict(dict)
        with open(
            Path(self.dataset_path) / "utterances.jsonl", "r", encoding="utf"
        ) as f:
            for _ in tqdm(range(0, total), total=total):
                u = json.loads(f.readline())
                if u["root"] == u["id"]:
                    utterances[u["root"]][u["id"]] = (
                        u["user"],
                        u["text"],
                        None,
                        u["meta"]["score"],
                    )
                else:
                    utterances[u["root"]][u["id"]] = (
                        u["user"],
                        u["text"],
                        u["reply_to"],
                        u["meta"]["score"],
                    )

        LOG.info(
            "Found %s conversations in dataset %s.",
            len(utterances),
            self.dataset_name,
        )

        LOG.info("Generating conversation threads")

        for _, posts in utterances.items():
            all_ids = []
            all_parent_ids = []
            for post_id, (_, _, parent, _) in posts.items():
                all_ids.append(post_id)
                all_parent_ids.append(parent)

            leafs = [p for p in all_ids if p not in all_parent_ids]
            if len(leafs) == 1:
                continue
            for leaf in leafs:
                conv = []
                l = leaf
                bad_thread = False
                try:
                    while l:
                        (user, text, parent, likes) = posts[l]
                        # Skip thread if person or comment was delted or removed
                        if (
                            user in ["[deleted]", "[removed]", "dequeued"]
                            or text
                            in [
                                "[deleted]",
                                "[removed]",
                            ]
                            or len(text.strip()) == 0
                        ):
                            bad_thread = True
                            break
                        conv.append((user, text, likes))
                        l = parent

                    if not bad_thread:
                        conversation = list(reversed(conv))
                        occurrences: list[Occurrence] = []
                        op = None
                        for user, text, likes in conversation:
                            if op is None:
                                op = user
                            if user == op:
                                occurrences.append(
                                    Participant(
                                        name="User",
                                        identifier=user.split()[0],
                                        emotion=None,
                                        says=text.replace("\n", "\\n"),
                                    )
                                )
                            else:
                                occurrences.append(
                                    Self(emotion=None, says=text.replace("\n", "\\n"))
                                )
                        yield Moment(str(uuid4()), occurrences)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    LOG.error(e)
