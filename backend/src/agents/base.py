"""
Abstract base class for all agents in the prediction system.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Base agent with logging and context management."""

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")

    @abstractmethod
    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute the agent's task and return enriched context."""
        ...

    def log(self, message: str) -> None:
        """Log an informational message."""
        self.logger.info(f"[{self.name}] {message}")

    def warn(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(f"[{self.name}] {message}")
