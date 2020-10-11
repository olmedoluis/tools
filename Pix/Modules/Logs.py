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


def get_fetcher(run, branch=[]):
    def fetcher(filters=[]):
        logs_raw = run(
            [
                "git",
                "log",
                "--first-parent",
                "--oneline",
                *filters,
                *branch,
                '--pretty=format:"%h/*/%an/*/%cr/*/%ci/*/%s"',
            ],
            False,
        )

        return [] if logs_raw == "" else get_logs(logs_raw.split("\n"))

    return fetcher


def log():
    from .Helpers import run, MessageControl
    from .Branch import get_branch_creator
    from .Prompts import logger
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()

    branch_creator, current_branch = get_branch_creator()
    specification = [] if branch_creator == "" else [f"{branch_creator}.."]

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

    logs = [] if logs_raw == "" else get_logs(logs_raw.split("\n"))

    logger(
        logs=logs,
        branch=m.get_message("branch-title", {"pm_branch": current_branch}),
        error_message=m.get_message("log-exit"),
        colors=INPUT_THEME["LOG_LOG"],
        icons=INPUT_ICONS,
        fetch=get_fetcher(run, specification),
    )

    m.log("log-exit")


def router(argument_parser, sub_route):
    if sub_route == "DEFAULT":
        log()
