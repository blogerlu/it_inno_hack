from abc import ABC, abstractmethod
from typing import Callable

import pandas as pd


class Rule(ABC):
    """Rule for comparing rows."""

    @abstractmethod
    def __init__(self, func: Callable[[pd.Series, pd.Series], float]) -> None:
        self.func = func

    @abstractmethod
    def __call__(self, row1: pd.Series, row2: pd.Series) -> float:
        return self.func(row1, row2)


class SimilaritySystem:
    """
    Similarity system. Use for registering
    """

    def __init__(self) -> None:
        self.rules = []

    def __call__(self, row1: pd.Series, row2: pd.Series) -> float:
        """Compare rows and calculate similarity. Return similarity in range [0, 1]."""
        # TODO: remove test rules and create real rules

        if row1["email"] == row2["email"]:
            return 1
        if row1["phone"] == row2["phone"]:
            return 1
        return 0

        # for rule in self.rules:
        #     similarity = rule(row1, row2)
        #     if similarity > self.SIMILARITY_THRESHOLD:
        #         return similarity
        #
        # return 0

    def add_rule(self, rule: Rule) -> None:
        """Add rule for comparing rows."""
        self.rules.append(rule)
