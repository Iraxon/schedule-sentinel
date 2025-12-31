from dataclasses import dataclass
from datetime import timedelta
from typing import Never, Self

type Token = TimeToken | AmPmToken | DescToken | NewlineToken | ErrorToken


@dataclass(frozen=True)
class TimeToken:
    time: timedelta
    """
    Hours/minutes from midnight (AM)
    or noon (PM)

    0 <= t < 12 hr
    """

    @classmethod
    def of(cls, s: str, line: int, col: int) -> Self:

        hour, minute = map(int, s.split(":"))

        return cls(timedelta(hours=hour if hour != 12 else 0, minutes=minute))


@dataclass(frozen=True)
class AmPmToken:
    is_pm: bool

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

    @classmethod
    def of(cls, s: str, line: int, col: int) -> None:

        return None  # Temporarily rigged to discard

        return cls()


@dataclass(frozen=True)
class ErrorToken:

    @classmethod
    def of(cls, s: str, line: int, col: int) -> Never:

        raise ValueError(f"Unexpected character: {s}")
