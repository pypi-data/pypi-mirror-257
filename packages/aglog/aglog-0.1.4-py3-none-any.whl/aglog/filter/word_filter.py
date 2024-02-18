from __future__ import annotations

import logging
from abc import abstractmethod
from typing import Literal

from typing_extensions import Self, override


class WordFilter(logging.Filter):
    def __init__(
        self: Self,
        *,
        includes: list[str] | None = None,
        excludes: list[str] | None = None,
        include_type: Literal["any", "all"] = "any",
    ) -> None:
        self.includes = includes or []
        self.excludes = excludes or []
        self.include_type = include_type

    @abstractmethod
    def get_target(self: Self, record: logging.LogRecord) -> str | None:
        raise NotImplementedError  # pragma: no cover

    def filter(self: Self, record: logging.LogRecord) -> bool:
        target = self.get_target(record)
        if target is None:
            return True  # pragma: no cover

        check_select = self.check_select(target)
        check_ignore = self.check_ignore(target)
        if self.includes != [] and self.excludes != []:
            return check_select and not check_ignore
        if self.includes == [] and self.excludes != []:
            return not check_ignore
        if self.includes != [] and self.excludes == []:
            return check_select
        return True

    def check_select(self: Self, target: str) -> bool:
        return any(w in target for w in self.includes) if self.include_type == "any" else all(w in target for w in self.includes)

    def check_ignore(self: Self, target: str) -> bool:
        return any(w in target for w in self.excludes)


class MessageWordFilter(WordFilter):
    @override
    def get_target(self: Self, record: logging.LogRecord) -> str | None:
        return record.getMessage()


class ThreadNameFilter(WordFilter):
    @override
    def get_target(self: Self, record: logging.LogRecord) -> str | None:
        return record.threadName


class ProcessNameFilter(WordFilter):
    @override
    def get_target(self: Self, record: logging.LogRecord) -> str | None:
        return record.processName


class NameFilter(WordFilter):
    @override
    def get_target(self: Self, record: logging.LogRecord) -> str | None:
        return record.name

    @override
    def check_select(self: Self, target: str) -> bool:
        if "" in self.includes:
            return True
        return any(w.split(".") == target.split(".")[: len(w.split("."))] for w in self.includes)

    @override
    def check_ignore(self: Self, target: str) -> bool:
        if "" in self.excludes:
            return True
        return any(w.split(".") == target.split(".")[: len(w.split("."))] for w in self.excludes)
