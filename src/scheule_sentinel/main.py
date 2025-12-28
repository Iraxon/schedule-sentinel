import concurrent.futures
import datetime
import functools
from math import floor
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


def prompt_number(prompt: str) -> int:

    while True:

        x = input(prompt)

        try:

            return int(x)

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


def demand_decision() -> int:

    future = executor.submit(
        functools.partial(
            prompt_number,
            prompt="Enter delay in minutes or 0 to discard event.\n\n> ",
        )
    )

    while not future.done():
        request_user_attention()

    return future.result()


test_schedule: dict[datetime.datetime, str] = {
    datetime.datetime.combine(
        datetime.datetime.today().date(), datetime.time(hour=hr, minute=min, second=s)
    ): f"Test event originally scheduled for {hr}:{min}:{s}"
    for hr in range(0, 24)
    for min in range(0, 60)
    for s in range(0, 60, 30)
}
"""
Test events every 30 seconds in the day
(the real format will not support seconds)
"""

TEST = True

if __name__ == "__main__":

    for time, event in test_schedule.items():
        print(f"{time} {event}")

    if TEST:
        schedule = test_schedule
    else:
        raise NotImplementedError

    while True:

        now = datetime.datetime.now()

        if now in schedule.keys(): # This comparison needs to be changed, as it misses all the time
            print(f"EVENT: {schedule[now]}")
            delay = demand_decision()

            if delay > 0:
                schedule[now + datetime.timedelta(minutes=delay)] = schedule[now]

            del schedule[now]

        if not TEST:
            sleep(10)
            # Second precision is needed for the test schedule so we don't sleep
