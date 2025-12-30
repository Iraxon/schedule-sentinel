import datetime
from dataclasses import dataclass

type Schedule = list[ScheduleEntry]  # Heap queue


@dataclass(frozen=True)
class ScheduleEntry:
    datetime: datetime.datetime
    desc: str

    def __lt__(self, other: ScheduleEntry) -> bool:
        return self.datetime < other.datetime

    def __eq__(self, other: object) -> bool:

        if isinstance(other, ScheduleEntry):
            return self.datetime == other.datetime

        return False

    def __str__(self) -> str:
        return f"{self.datetime} {self.desc}"
