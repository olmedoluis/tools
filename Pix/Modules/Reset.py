def parse_status(status):
    from os.path import isdir

    reset_commands = []

    for status_id in status:
        if status_id == "branch":
            continue

        for change in status[status_id]:
            if status_id == "untracked":
                folder_delete = ["-r", "-f"] if isdir(change) else []

                reset_commands.append(["rm", *folder_delete, change])
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


def reset(
    file_paths=[],
    use_availables=False,
    force_selection=False,
    show_logs=True,
    files_shown=[],
):
    from .Prompts import multi_select
    from .Helpers import MessageControl
    from .Status import get_status, search_in_status, get_status_paths
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    status = get_status(ignoreColors=True)

    file_paths = (
        search_in_status(file_paths, status, excluded_files=["branch", "added"])
        if len(file_paths)
        else get_status_paths(status, excluded_files=["branch", "added"])
    )

    if len(file_paths) == 0:
        m.log("error-reset-files_not_found")
        exit()

    elif use_availables:
        pass

    elif len(file_paths) != 1 or force_selection:
        print()
        answers = multi_select(
            title=m.get_message("reset-title"),
            final_title=m.get_message("file-selection-finaltitle"),
            error_message=m.get_message("error-files_selected_not_found"),
            options=file_paths,
            colors=INPUT_THEME["RESET_SELECTION"],
            icons=INPUT_ICONS,
        )

        if len(answers) == 0:
            return m.log("error-files_selected_not_found")

        file_paths = answers

    executeReset(file_paths, status)
    if show_logs:
        m.log("reset-success")
        m.logMany(
            message_id="reset-file",
            param_name="pm_file",
            contents=files_shown + file_paths,
        )

    return file_paths


def reset_individually(file_paths):
    if len(file_paths):
        index = 1
        files_resetted = []

        for file_path in file_paths:
            file_resetted = reset(
                file_paths=[file_path],
                show_logs=len(file_paths) == index,
                files_shown=files_resetted,
            )

            files_resetted = files_resetted + file_resetted
            index = index + 1

        return

    reset(force_selection=True)


def router(argument_manager, sub_route):
    if sub_route == "RESET_ALL":
        reset(argument_manager.left_keys[1:], use_availables=True)
    elif sub_route == "DEFAULT":
        reset_individually(argument_manager.left_keys)
