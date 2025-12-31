from dataclasses import dataclass
from datetime import datetime, time, timedelta
from heapq import heappush
from typing import TYPE_CHECKING

from .token_classes import AmPmToken, DescToken, TimeToken
from classes import Schedule, ScheduleEntry

if TYPE_CHECKING:
    from .tokenization import Token


@dataclass
class ParseState:
    """
    Mutable state holder for the parser
    """

    tokens: tuple[Token, ...]
    cursor: int = 0
    line: int = 0
    column: int = 0

    def next(self) -> Token:
        out = self.tokens[self.cursor]
        self.cursor += 1
        return out


def parse_schedule(ts: tuple[Token, ...]) -> Schedule:
    out: Schedule = []

    state = ParseState(ts)

    while state.cursor < len(ts):
        heappush(out, parse_schedule_entry(state))

    return out


def parse_schedule_entry(state: ParseState) -> ScheduleEntry:

    time_token: TimeToken
    am_pm_token: AmPmToken
    desc_token: DescToken

    if isinstance(t := state.next(), TimeToken):
        time_token = t

        if isinstance(t := state.next(), AmPmToken):
            am_pm_token = t

            if isinstance(t := state.next(), DescToken):
                desc_token = t

                time_delta: timedelta = time_token.time
                is_pm = am_pm_token.is_pm

                midnight_today = datetime.combine(datetime.now(), time(0, 0))

                dt: datetime = (
                    midnight_today
                    if not is_pm
                    else midnight_today + timedelta(hours=12)  # Noon
                ) + time_delta

                return ScheduleEntry(dt, desc_token.value)

    raise ValueError(f"Unexpected {t}")
