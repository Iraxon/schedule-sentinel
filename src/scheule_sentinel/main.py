import concurrent.futures
import datetime
import functools
import heapq
import winsound
from time import sleep

from prompting import prompt_minutes_seconds

from test_schedule import test_schedule as test_schedule
from classes import ScheduleEntry

executor = concurrent.futures.InterpreterPoolExecutor(2)


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


TEST = True


def main() -> None:
    if TEST:
        schedule = test_schedule()
    else:
        raise NotImplementedError
        # Remember to use heapq operations!

    for entry in schedule:
        print(entry)

    while True:

        now = datetime.datetime.now()

        print(now)

        if len(schedule) == 0:
            print(f"Schedule is empty!")
            demand_acknowledgement()
            break

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
                print(f"Delayed to {postponed}")
                heapq.heapreplace(schedule, postponed)

            else:
                heapq.heappop(schedule)
                print(f"Dismissed")

        # Higher precision is needed for testing
        if not TEST:
            sleep(10)
        else:
            sleep(0.5)


if __name__ == "__main__":
    main()
