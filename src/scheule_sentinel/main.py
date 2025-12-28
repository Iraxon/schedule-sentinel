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
            prompt="Positive number to postpone by x minutes. 0 to discard event",
        )
    )

    while not future.done():
        request_user_attention()

    return future.result()


test_schedule: dict[datetime.time, str] = {
    datetime.time(hr, min, s): f"Test event originally scheduled for {hr}:{min}:{s}"
    for hr in range(0, 24)
    for min in range(0, 60)
    for s in range(0, 60, 30)
}
"""
Test events every 30 seconds in the day
(the real format will not support seconds)
"""

if __name__ == "__main__":

    for time, event in test_schedule.items():
        print(f"{time} {event}")

    schedule = test_schedule

    while True:

        print(demand_decision())

        sleep(10)
