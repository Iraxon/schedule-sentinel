from classes import Schedule
from _parsing.semantics import parse_schedule
from _parsing.tokenization import tokenize


def parse(input: str) -> Schedule:
    return parse_schedule(tokenize(input))


if __name__ == "__main__":

    print(parse("12:00 PM Exercise\n1:00 PM Lunch\n3:00 PM Chaplet of Divine Mercy"))
