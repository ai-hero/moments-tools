import yaml
from abc import ABC, abstractmethod
from typing import Type
from moments.moment import Moment, Self

DEFAULT_NAME = "Leela"


class AgentConfig:
    kind: str = None
    id: str = ""
    variant: str = ""
    init: str = ""

    @staticmethod
    def from_file(config_file: str) -> "AgentConfig":
        with open(config_file, "r", encoding="utf-8") as file:
            return AgentConfig(**yaml.safe_load(file))

    # pylint: disable=redefined-builtin
    def __init__(
        self: "AgentConfig",
        kind: str,
        id: str,
        variant: str,
        init: str,
    ):
        self.kind = kind
        self.id = id
        self.variant = variant
        self.init = init


class Agent(ABC):
    instance_id: str = None
    config: dict = None

    def __init__(
        self: "Agent",
        instance_id: str,
        name: str,
        config: AgentConfig,
    ):
        self.instance_id = instance_id
        self.name = name
        self.config = config

    @abstractmethod
    def respond(self: "Agent", moment: Moment) -> Self:
        pass


class AgentFactory:
    agent_classes = {}

    @classmethod
    def register(cls: Type, agent_cls: Type):
        cls.agent_classes[agent_cls.__name__] = agent_cls

    @classmethod
    def create(cls: Type, agent_instance_id: str, agent_config: AgentConfig) -> "Agent":
        return cls.agent_classes[agent_config.kind](
            instance_id=agent_instance_id,
            name=DEFAULT_NAME,
            config=agent_config,
        )
