def remove(
    file_paths=[],
    use_availables=False,
    force_selection=False,
    show_logs=True,
    files_shown=[],
):
    from .Prompts import multi_select
    from .Helpers import run, parse_selection_options, MessageControl
    from .Status import get_status, search_in_status, get_status_paths
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    status = get_status(ignoreColors=True)

    is_individual_path = len(file_paths) == 1
    file_paths = (
        search_in_status(file_paths, status, included_files=["added"])
        if len(file_paths)
        else get_status_paths(status, included_files=["added"])
    )

    if len(file_paths) == 0:
        m.log("error-remove-files_not_found")
        exit()

    elif use_availables:
        pass

    elif len(file_paths) != 1 or force_selection:
        print()
        answers = multi_select(
            title=m.get_message("remove-title"),
            final_title=m.get_message("file-selection-finaltitle"),
            error_message=m.get_message("error-files_selected_not_found"),
            options=parse_selection_options(file_paths),
            colors=INPUT_THEME["REMOVE_SELECTION"],
            icons=INPUT_ICONS,
        )

        if len(answers) == 0:
            return m.log("error-files_selected_not_found")

        file_paths = answers

    run(["git", "reset", "--"] + file_paths)
    if show_logs:
        m.log("remove-success")
        m.logMany(
            message_id="remove-file",
            param_name="pm_file",
            contents=files_shown + file_paths,
        )

    return file_paths


def remove_individually(file_paths):
    if len(file_paths):
        index = 1
        files_removed = []

        for file_path in file_paths:
            file_removed = remove(
                file_paths=[file_path],
                show_logs=len(file_paths) == index,
                files_shown=files_removed,
            )

            files_removed = files_removed + file_removed
            index = index + 1

        return

    remove(force_selection=True)


def router(argument_manager, sub_route):
    if sub_route == "REMOVE_ALL":
        remove(argument_manager.left_keys[1:], use_availables=True)
    if sub_route == "DEFAULT":
        remove_individually(argument_manager.left_keys)
