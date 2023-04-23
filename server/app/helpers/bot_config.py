import yaml
import pathlib
from typing import Type

SEP_SECTION = "----------"


class BotConfig:
    """
    Config for a bot containing:
    - instructions: The system instructions about who the bot is. These will be used to auto-generate system instructions.
    - roles: The roles that the user and ai have.
    - example: An example interaction containing
        - context: an optional real-time context for each interaction (could change during conversation).
        - messages: a list of messages each containing:
            - who: is it the User or AI
            - conent: The content of the message.
    - begin: an optional begin message if it's AI should speak first.
    - separator: an optional separator that helps frame the conversation.
    """

    version: str = ""
    config: dict = None

    @classmethod
    def from_file(cls: Type, config_file: str) -> "BotConfig":
        with open(
            pathlib.Path(__file__).parent.resolve() / "configs" / config_file,
            "r",
            encoding="utf-8",
        ) as file:
            return BotConfig(yaml.safe_load(file))

    def __init__(self: "BotConfig", config_dict: dict):
        self.version = config_dict["version"]
        self.config = config_dict["config"]
        self.assistant = self.config["roles"]["assistant"]
        self.user = self.config["roles"]["user"]

    def _build_examples(self: "BotConfig", examples: list[dict]):
        return "\n".join([self._build_example(example) for example in examples])

    def _build_example(self: "BotConfig", conversation: dict):
        return f"""{SEP_SECTION}
{SEP_SECTION}
Context: {conversation.get("context", "-")}
{SEP_SECTION}
Messages:
{self._build_text_messages(conversation["messages"])}
{SEP_SECTION}
{SEP_SECTION}"""

    def _build_text_messages(self: "BotConfig", messages: list[dict]):
        return "\n".join(
            [
                f"""{self.config["roles"][message["role"]]}: {message["content"]}"""
                for message in messages
                if message["role"] != "system"
            ]
        )

    def build_prompt(
        self: "BotConfig",
        conversation: dict,
    ):
        return f"""{self.get_system_message(conversation.get("context", None))}
Messages:
{self._build_text_messages(conversation["messages"])}
{self.config["roles"]['assistant']}: """.strip()

    def get_system_message(self: "BotConfig", context: str):
        if self.version:  # works on any config version
            return f"""{self.config.get("instructions", "").strip()}
{self._build_examples(self.config.get("examples", []))}
{self.config.get("begin", "").strip()}
{SEP_SECTION}
{SEP_SECTION}
Context: {context if context else "-"}
{SEP_SECTION}
"""
