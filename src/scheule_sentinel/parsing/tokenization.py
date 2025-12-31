from collections.abc import Callable, Iterator
import re
from dataclasses import dataclass
from datetime import datetime, time
from typing import Never, Self, cast

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


type TokenConstructor[T: Token] = Callable[[str, int, int], T | None]
"""
Retun None to refrain from adding a Token
"""


def discard(s: str, line: int, col: int) -> None:
    return None


TOKEN_MANIFEST: tuple[tuple[str, str, TokenConstructor[Token]], ...] = (
    ("time_token", r"\d{1,2}:\d{2}", TimeToken.of),
    ("am_pm_token", r"AM|PM", AmPmToken.of),
    ("comment_token", r"(?:#|//)[^\n]*?(?=\n)|/\*(?:.|\n)*?\*/", discard),
    ("newline_token", r"\n", NewlineToken.of),
    ("whitespace_token", r"\s+", discard),
    ("desc_token", r"(?:\w| )+", DescToken.of),
    ("error_token", r".", ErrorToken.of),
)
"""
Each entry must have a unqiue shortname, a regex pattern,
and a TokenConstructor function to process the match into a Token
object (or None, in the case of comments or the like)
"""

TOKEN_CONSTRUCTOR_MAP = {name: type for name, _, type in TOKEN_MANIFEST}

TOKEN_REGEX = re.compile(
    "|".join(rf"(?P<{name}>{pattern})" for name, pattern, _ in TOKEN_MANIFEST)
)


def tokenize(input: str) -> tuple[Token, ...]:
    return refined_from_raw(raw_tokenize(input))


def raw_tokenize(input: str) -> Iterator[Token]:

    line_start = 0  # Neither of these are really used yet
    line_num = 1  # Newlines need to be set up to update it

    for match_object in re.finditer(TOKEN_REGEX, input):

        constructor = TOKEN_CONSTRUCTOR_MAP[cast(str, match_object.lastgroup)]
        lexeme = match_object.group()
        col_num = match_object.start() - line_start

        print(f"matched {lexeme}")

        token = constructor(lexeme, line_num, col_num)

        if token is None:
            print("Discarding")
            pass
        else:
            print(f"Yielding {token}")
            yield token


def refined_from_raw(raw: Iterator[Token]) -> tuple[Token, ...]:

    raw_tuple = tuple(raw)

    without_blank_lines = tuple(
        t
        for i, t in enumerate(raw_tuple)
        if not isinstance(t, NewlineToken)
        or i == len(raw_tuple) - 1
        or not isinstance(raw_tuple[i + 1], NewlineToken)
    )

    with_trailing_newline = (
        without_blank_lines
        if isinstance(without_blank_lines[-1], NewlineToken)
        else without_blank_lines + (NewlineToken(),)
    )

    return with_trailing_newline


if __name__ == "__main__":

    print(TOKEN_CONSTRUCTOR_MAP)

    print("===")

    tokens = tokenize("1:00 PM Lunch\n3:00 PM Chaplet of Divine Mercy")

    print("===")

    print(
        "\n".join(
            str(t) for t in tokens
        )
    )
