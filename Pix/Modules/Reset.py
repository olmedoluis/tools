def parse_status(status):
    reset_commands = []

    for status_id in status:
        for change in status[status_id]:
            if status_id == "untracked":
                reset_commands.append(["rm", change])
            else:
                reset_commands.append(["git", "checkout", change])

    return reset_commands


def reset(file_paths=[], should_verify=True, messages=""):
    from .Prompts import multiSelect
    from .Helpers import runAll, removeColors, MessageControl
    from .Status import get_status, search_in_status
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl() if messages == "" else messages
    status = get_status()

    files_for_parsing = []

    if len(file_paths) == 0:
        for status_id in status:
            status_content = status[status_id]
            if status_id == "branch" or status_id == "added":
                continue

            file_paths = file_paths + status_content

    if len(file_paths) != 0:
        files_for_parsing = search_in_status(
            file_paths,
            status,
            excluded_files=["branch", "added"],
            get_original_structure=True,
        )
        file_paths = search_in_status(
            file_paths, status, excluded_files=["branch", "added"]
        )

    if not should_verify:
        commands = parse_status(files_for_parsing)

        runAll(commands)
        return m.log("reset-all-success")

    if len(file_paths) == 0:
        return m.log("error-reset-files_not_found")

    print()
    answers = multiSelect(
        title=m.getMessage("reset-title"),
        finalTitle=m.getMessage("file-selection-finaltitle"),
        errorMessage=m.getMessage("error-files_selected_not_found"),
        options=file_paths,
        colors=INPUT_THEME["RESET_SELECTION"],
        icons=INPUT_ICONS,
    )

    if len(answers) == 0:
        return m.log("error-files_selected_not_found")

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    files_for_parsing = search_in_status(
        choices,
        status,
        excluded_files=["branch", "added"],
        get_original_structure=True,
    )

    runAll(parse_status(files_for_parsing))
    m.log("reset-success")


def reset_all():
    reset(file_paths=[], should_verify=False)


def router(argument_manager, sub_route):
    if sub_route == "RESET_ALL":
        reset_all()
    elif sub_route == "DEFAULT":
        reset(argument_manager.left_keys)
