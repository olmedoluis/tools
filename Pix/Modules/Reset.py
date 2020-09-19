def parse_status(status):
    reset_commands = []

    for status_id in status:
        for change in status[status_id]:
            if status_id == "untracked":
                reset_commands.append(["rm", change])
            else:
                reset_commands.append(["git", "checkout", change])

    return reset_commands


def executeReset(file_paths, status):
    from .Status import search_in_status
    from .Helpers import runAll

    files_for_parsing = search_in_status(
        file_paths,
        status,
        excluded_files=["branch", "added"],
        get_original_structure=True,
    )

    commands = parse_status(files_for_parsing)

    runAll(commands)


def reset(file_paths=[], use_availables=False, messages=""):
    from .Prompts import multi_select
    from .Helpers import removeColors, MessageControl
    from .Status import get_status, search_in_status, get_status_paths
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl() if messages == "" else messages
    status = get_status()

    is_individual_path = len(file_paths) == 1
    file_paths = (
        search_in_status(file_paths, status, excluded_files=["branch", "added"])
        if len(file_paths)
        else get_status_paths(status, excluded_files=["branch", "added"])
    )

    if len(file_paths) == 0:
        return m.log("error-reset-files_not_found")
    elif use_availables:
        executeReset(file_paths, status)
        return m.log("reset-all-success")
    elif is_individual_path and len(file_paths) == 1:
        return executeReset(file_paths, status)

    print()
    answers = multi_select(
        title=m.getMessage("reset-title"),
        final_title=m.getMessage("file-selection-finaltitle"),
        error_message=m.getMessage("error-files_selected_not_found"),
        options=file_paths,
        colors=INPUT_THEME["RESET_SELECTION"],
        icons=INPUT_ICONS,
    )

    if len(answers) == 0:
        return m.log("error-files_selected_not_found")

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    executeReset(choices, status)
    m.log("reset-success")


def reset_all():
    reset(file_paths=[], use_availables=True)


def reset_individually(file_paths):
    from .Helpers import MessageControl

    m = MessageControl()

    if len(file_paths):
        for file_path in file_paths:
            reset(file_paths=[file_path], messages=m)

        return m.log("reset-success")

    reset(messages=m)


def router(argument_manager, sub_route):
    if sub_route == "RESET_ALL":
        reset(use_availables=True)
    elif sub_route == "DEFAULT":
        reset_individually(argument_manager.left_keys)
