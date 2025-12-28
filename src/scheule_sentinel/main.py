import concurrent.futures
from dataclasses import dataclass
import datetime
import heapq
import functools
import winsound
from time import sleep


executor = concurrent.futures.InterpreterPoolExecutor(2)


def prompt_yes_no(prompt: str) -> bool:

    while True:

        match input(prompt):

            case "Y" | "y":
                return True

            case "N" | "n":
                return False

            case _:
                print("Invalid input.")


def prompt_minutes_seconds(prompt: str) -> int:
    """
    Input is in minutes, unless suffixed with 's'

    Output is in seconds
    """

    seconds = False

    while True:

        x = input(prompt)

        if x.endswith("s"):
            x = x[:-1]
            seconds = True

        try:
            x = int(x)
            return x * 60 if not seconds else x

        except ValueError:
            print("Invalid input.")


def request_user_attention() -> None:
    """
    Takes one second
    """
    winsound.Beep(880, 333)
    winsound.Beep(440, 333)
    winsound.Beep(220, 333)
    sleep(1)


def demand_delay_decision() -> int:

    future = executor.submit(
        functools.partial(
            prompt_minutes_seconds,
            prompt=(
                "Enter 0 to dismiss, a number in minutes to delay,\n"
                "or a number suffixed with s to delay in seconds.\n\n> "
            ),
        )
    )

    while not future.done():
        request_user_attention()

    return future.result()


def demand_acknowledgement() -> None:

    future = executor.submit(functools.partial(input, "Press Enter to acknowledge."))

    while not future.done():
        request_user_attention()


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


def test_schedule() -> Schedule:
    """
    One event five seconds into the future
    """
    return [
        ScheduleEntry(
            datetime.datetime.now() + datetime.timedelta(seconds=5), f"Test event"
        )
    ]


TEST = True

if __name__ == "__main__":

    if TEST:
        schedule = test_schedule()
    else:
        raise NotImplementedError
        # Remember to use heapq operations!

    for entry in schedule:
        print(f"{entry.datetime} {entry.desc}")

    while True:

        now = datetime.datetime.now()

        print(now)

        if len(schedule) == 0:
            while True:
                request_user_attention()

        if (
            schedule[0].datetime < now
        ):  # Guaranteed to compare the earliest, because heapq
            print(f"EVENT: {schedule[0].desc}")

            delay = demand_delay_decision()
            if delay > 0:
                postponed = ScheduleEntry(
                    datetime.datetime.now() + datetime.timedelta(seconds=delay),
                    schedule[0].desc,
                )
                heapq.heapreplace(schedule, postponed)
            else:
                heapq.heappop(schedule)

        # Higher precision is needed for testing
        if not TEST:
            sleep(10)
        else:
            sleep(0.5)
