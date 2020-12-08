def add(
    file_paths=[],
    use_availables=False,
    force_selection=False,
    show_logs=True,
    files_shown=[],
):
    from .Prompts import multi_select
    from .Helpers import run, removeColors, parse_for_select_options, MessageControl
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
        m.log("error-add-files_not_found")
        exit()

    elif use_availables:
        pass

    elif len(file_paths) != 1 or force_selection:
        print()
        answers = multi_select(
            title=m.get_message("add-title"),
            final_title=m.get_message("file-selection-finaltitle"),
            error_message=m.get_message("error-files_selected_not_found"),
            options=parse_for_select_options(file_paths),
            colors=INPUT_THEME["ADD_SELECTION"],
            icons=INPUT_ICONS,
        )

        if len(answers) == 0:
            return m.log("error-files_selected_not_found")

        file_paths = answers

    run(["git", "add"] + file_paths)
    if show_logs:
        m.log("add-success")
        m.logMany(
            message_id="add-file",
            param_name="pm_file",
            contents=files_shown + file_paths,
        )

    return file_paths


def add_individually(file_paths):
    if len(file_paths):
        index = 1
        files_added = []

        for file_path in file_paths:
            file_added = add(
                file_paths=[file_path],
                show_logs=len(file_paths) == index,
                files_shown=files_added,
            )

            files_added = files_added + file_added
            index = index + 1

        return

    add(force_selection=True)


def router(argument_manager, sub_route):
    if sub_route == "ADD_ALL":
        add(argument_manager.left_keys[1:], use_availables=True)
    if sub_route == "DEFAULT":
        add_individually(argument_manager.left_keys)
