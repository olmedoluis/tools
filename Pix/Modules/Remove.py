def remove(file_paths=[], should_verify=True):
    from .Prompts import multi_select
    from .Helpers import run, removeColors, MessageControl
    from .Status import get_status, search_in_status
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    status = get_status()

    specific_files = file_paths if file_paths else []
    if len(file_paths) != 0 and should_verify:
        specific_files = search_in_status(file_paths, status, included_files=["added"])

    if len(specific_files) == 1 or not should_verify:
        run(["git", "reset"] + specific_files)
        return m.log("remove-success")

    options = status["added"] if "added" in status else []
    options = specific_files if len(specific_files) != 0 else options

    if len(options) == 0:
        return m.log("error-remove-files_not_found")

    print()
    answers = multi_select(
        title=m.getMessage("remove-title"),
        final_title=m.getMessage("file-selection-finaltitle"),
        error_message=m.getMessage("error-files_selected_not_found"),
        options=options,
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


def remove_all(file_search):
    from .Helpers import run, removeColors, MessageControl
    from .Status import get_status, search_in_status

    m = MessageControl()
    status = get_status()

    if len(file_search) > 0:
        matches = search_in_status(file_search, status, included_files=["added"])

        return (
            m.log("error-file_match_not_found")
            if len(matches) == 0
            else remove(matches, False)
        )

    has_files_to_remove = False
    for status_id in status:
        if status_id != "added":
            continue

        has_files_to_remove = True
        break

    if has_files_to_remove:
        run(["git", "reset", "."])
        m.log("remove-all-success")
    else:
        m.log("error-remove-files_not_found")


def router(argument_manager, sub_route):
    if sub_route == "REMOVE_ALL":
        remove_all(argument_manager.left_keys[1:])
    if sub_route == "DEFAULT":
        remove(argument_manager.left_keys)
