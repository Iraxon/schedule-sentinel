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
