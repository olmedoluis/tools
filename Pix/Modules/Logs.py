class Log:
    def __init__(self, hash, author, time, commit, date):
        self.hash = hash
        self.author = author
        self.time = time
        self.date = date
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
                date=log_array[3],
                commit=log_array[4][:-1],
            )
        )

    return logs


def log():
    from .Helpers import run
    from .Branch import get_branch_creator
    from .Prompts import logger

    branch_creator, current_branch = get_branch_creator()
    is_from_remote = "git@github.com:" in branch_creator
    specification = [] if is_from_remote else [f"{branch_creator}.."]

    logs_raw = run(
        [
            "git",
            "log",
            "--first-parent",
            "--oneline",
            *specification,
            '--pretty=format:"%h/*/%an/*/%cr/*/%ci/*/%s"',
        ]
    )

    logs = get_logs(logs_raw.split("\n"))

    logger(
        error_message="error message",
        logs=logs,
        branch=current_branch,
    )


def router(argument_parser, sub_route):
    if sub_route == "DEFAULT":
        log()
