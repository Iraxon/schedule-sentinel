from collections.abc import Iterator
import re
from dataclasses import dataclass
from datetime import datetime, time
from typing import Never, Self, cast

type Token = TimeToken | DescToken | NewlineToken | WhitespaceToken | CommentToken | ErrorToken


@dataclass(frozen=True)
class TimeToken:
    time: datetime

    @classmethod
    def of(cls, s: str) -> Self:

        hour, minute = map(int, s.split(":"))

        return cls(datetime.combine(datetime.now(), time(hour=hour, minute=minute)))


@dataclass(frozen=True)
class DescToken:
    value: str

    @classmethod
    def of(cls, s: str) -> Self:

        return cls(s)


@dataclass(frozen=True)
class NewlineToken:
    pass

    @classmethod
    def of(cls, _: str) -> Self:

        return cls()


@dataclass(frozen=True)
class CommentToken:
    pass

    @classmethod
    def of(cls, _: str) -> None:

        return None


@dataclass(frozen=True)
class WhitespaceToken:
    pass

    @classmethod
    def of(cls, _: str) -> None:

        return None


@dataclass(frozen=True)
class ErrorToken:
    pass

    @classmethod
    def of(cls, s: str) -> Never:

        raise ValueError(f"Unexpected character: {s}")


def token_of(type_str: str, lexeme: str, _: int, __: int) -> Token | None:

    type = TOKEN_TYPE_MAP[type_str]

    return type.of(lexeme)


CAMEL_CASE_PATTERN = re.compile(r"(?<=[a-z])(?=[A-Z])")


def snake_from_camel(n: str) -> str:
    return ("_".join(re.split(CAMEL_CASE_PATTERN, n))).lower()


TOKEN_TYPE_MAP = {
    snake_from_camel(type.__name__): type
    for type in cast(
        tuple[type[Token], ...],
        (TimeToken, DescToken, NewlineToken, WhitespaceToken, CommentToken, ErrorToken),
    )
}

TOKENS: tuple[tuple[str, str], ...] = (
    ("time_token", r"\d{1,2}:\d{2}"),
    ("comment_token", r"(?:#|//)[^\n]*?(?=\n)|/\*(?:.|\n)*?\*/"),
    ("newline_token", r"\n"),
    ("whitespace_token", r"\s+"),
    ("desc_token", r"(?:\w| )*"),
    ("error_token", r"."),
)


TOKEN_REGEX = re.compile(
    "|".join(rf"(?P<{name}>{pattern})" for name, pattern in TOKENS)
)


def tokenize(input: str) -> tuple[Token, ...]:
    return process_raw(raw_tokenize(input))


def raw_tokenize(input: str) -> Iterator[Token]:

    line_start = 0  # Neither of these are really used yet
    line_num = 1  # Newlines need to be set up to update it

    for match_object in re.finditer(TOKEN_REGEX, input):

        type_string = cast(str, match_object.lastgroup)
        lexeme = match_object.group()
        col_num = match_object.start() - line_start

        print(f"matched {lexeme} as {type_string}")

        token = token_of(type_string, lexeme, line_num, col_num)

        if token is None:
            pass
        else:
            yield token


def process_raw(raw: Iterator[Token]) -> tuple[Token, ...]:

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

    print(TOKEN_TYPE_MAP)

    print(
        tokenize(
            """1:00 PM Lunch
        3:00 PM Chaplet of Divine Mercy
        """
        )
    )
