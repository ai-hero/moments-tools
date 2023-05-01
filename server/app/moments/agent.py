import yaml
from abc import ABC, abstractmethod
from typing import Type
from moments.moment import Moment, Self


class AgentConfig:
    config: dict = None

    @staticmethod
    def from_file(config_file: str) -> "AgentConfig":
        with open(config_file, "r", encoding="utf-8") as file:
            return AgentConfig(yaml.safe_load(file))

    def __init__(self: "AgentConfig", config: dict):
        self.config = config


class Agent(ABC):
    agent_config = None

    def __init__(self: "Agent", agent_config: AgentConfig):
        self.agent_config = agent_config

    @abstractmethod
    def respond(self: "Agent", moment: Moment) -> Self:
        pass


class AgentFactory:
    agent_classes = {}

    @classmethod
    def register(cls: Type, agent_cls: Type):
        cls.agent_classes[agent_cls.__name__] = agent_cls

    @classmethod
    def create(cls: Type, agent_config: AgentConfig) -> "Agent":
        return cls.agent_classes[agent_config.config["kind"]](agent_config)
