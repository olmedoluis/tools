def remove(file_paths=[], use_availables=False, messages=""):
    from .Prompts import multi_select
    from .Helpers import run, removeColors, MessageControl
    from .Status import get_status, search_in_status, get_status_paths
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl() if messages == "" else messages
    status = get_status()

    is_individual_path = len(file_paths) == 1
    file_paths = (
        search_in_status(file_paths, status, included_files=["added"])
        if len(file_paths)
        else get_status_paths(status, included_files=["added"])
    )

    if len(file_paths) == 0:
        return m.log("error-remove-files_not_found")
    elif use_availables:
        run(["git", "reset"] + file_paths)
        return m.log("remove-all-success")
    elif is_individual_path and len(file_paths) == 1:
        return run(["git", "reset"] + file_paths)

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


def remove_individually(file_paths):
    from .Helpers import MessageControl

    m = MessageControl()

    if len(file_paths):
        for file_path in file_paths:
            remove(file_paths=[file_path], messages=m)

        return m.log("remove-success")

    remove(messages=m)


def router(argument_manager, sub_route):
    if sub_route == "REMOVE_ALL":
        remove(file_paths=[], use_availables=True)
    if sub_route == "DEFAULT":
        remove_individually(argument_manager.left_keys)
