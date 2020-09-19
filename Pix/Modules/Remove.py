def remove(file_paths=[], should_verify=True):
    from .Prompts import multi_select
    from .Helpers import run, removeColors, MessageControl
    from .Status import get_status, search_in_status, get_status_paths
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    status = get_status()

    file_paths = (
        search_in_status(file_paths, status, included_files=["added"])
        if len(file_paths)
        else get_status_paths(status, included_files=["added"])
    )

    if len(file_paths) == 0:
        return m.log("error-remove-files_not_found")
    elif not should_verify:
        run(["git", "reset"] + file_paths)
        return m.log("remove-all-success")

    print()
    answers = multi_select(
        title=m.getMessage("remove-title"),
        final_title=m.getMessage("file-selection-finaltitle"),
        error_message=m.getMessage("error-files_selected_not_found"),
        options=file_paths,
        colors=INPUT_THEME["REMOVE_SELECTION"],
        icons=INPUT_ICONS,
    )

    if len(answers) == 0:
        return m.log("error-files_selected_not_found")

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(["git", "reset"] + choices)
    m.log("remove-success")


def router(argument_manager, sub_route):
    if sub_route == "REMOVE_ALL":
        remove(file_paths=[], should_verify=False)
    if sub_route == "DEFAULT":
        remove(argument_manager.left_keys)
