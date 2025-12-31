from dataclasses import dataclass
from typing import TYPE_CHECKING
from ..classes import Schedule, ScheduleEntry

if TYPE_CHECKING:
    from .tokenization import Token

@dataclass
class ParseState:
    """
    Mutable state holder for the parser
    """
    tokens: tuple[Token, ...]
    cursor: int
    line: int
    column: int

    def next(self) -> Token:
        out = self.tokens[self.cursor]
        self.cursor += 1
        return out

def parse_schedule(ts: tuple[Token, ...]) -> Schedule:
    out: Schedule = []

    for i, t in enumerate(ts):
        pass

    return out

def parse_schedule_entry(state: ParseState) -> ScheduleEntry:

    if isinstance(t := state.next(), TimeToken)

    raise ValueError(f"Unexpected {t}")
