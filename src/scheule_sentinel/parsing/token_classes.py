from dataclasses import dataclass
from datetime import datetime, time
from typing import Never, Self

type Token = TimeToken | AmPmToken | DescToken | NewlineToken | ErrorToken


@dataclass(frozen=True)
class TimeToken:
    time: datetime

    @classmethod
    def of(cls, s: str, line: int, col: int) -> Self:

        hour, minute = map(int, s.split(":"))

        return cls(datetime.combine(datetime.now(), time(hour=hour, minute=minute)))


@dataclass(frozen=True)
class AmPmToken:
    value: bool
    """
    True for PM
    """

    @classmethod
    def of(cls, s: str, line: int, col: int) -> Self:

        return cls(s == "PM")


@dataclass(frozen=True)
class DescToken:
    value: str

    @classmethod
    def of(cls, s: str, line: int, col: int) -> Self:

        return cls(s)


@dataclass(frozen=True)
class NewlineToken:
    pass

    @classmethod
    def of(cls, s: str, line: int, col: int) -> Self:

        return cls()


@dataclass(frozen=True)
class ErrorToken:
    pass

    @classmethod
    def of(cls, s: str, line: int, col: int) -> Never:

        raise ValueError(f"Unexpected character: {s}")
