class Log:
    def __init__(self, hash, author, time, commit):
        self.hash = hash
        self.author = author
        self.time = time
        self.commit = commit


def get_logs(logs_data):
    logs = []

    for log_line in logs_data:
        log_array = log_line.split("/*/")

        logs.append(
            Log(
                hash=log_array[0],
                author=log_array[1],
                time=log_array[2],
                commit=log_array[3][:-1],
            )
        )

    return logs


def log():
    from .Helpers import run
    from .Branch import get_branch_creator
    from .Prompts import logger

    branch_creator = get_branch_creator()
    logs_raw = run(
        [
            "git",
            "log",
            "--first-parent",
            "--oneline",
            f"{branch_creator}..",
            '--pretty=format:"%h/*/%an/*/%ar/*/%s"',
        ]
    )

    logs = get_logs(logs_raw.split("\n"))

    logger(error_message="wea", logs=logs, branch=branch_creator)


def router(argument_parser, sub_route):
    if sub_route == "DEFAULT":
        log()
