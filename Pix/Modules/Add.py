def add(file_paths=[], should_verify=True, messages=""):
    from .Prompts import multi_select
    from .Helpers import run, removeColors, MessageControl
    from .Status import get_status, search_in_status
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl() if messages == "" else messages
    status = get_status()

    specific_files = file_paths if file_paths else []
    if len(file_paths) != 0 and should_verify:
        specific_files = search_in_status(
            file_paths, status, excluded_files=["branch", "added"]
        )

    if len(specific_files) == 1 or not should_verify:
        run(["git", "add"] + specific_files)
        return m.log("add-success")

    options = specific_files
    if len(specific_files) == 0:
        for status_id in status:
            statusContent = status[status_id]
            if status_id == "branch" or status_id == "added":
                continue

            options = options + statusContent

    if len(options) == 0:
        return m.log("error-add-files_not_found")

    print()
    answers = multi_select(
        title=m.getMessage("add-title"),
        final_title=m.getMessage("file-selection-finaltitle"),
        error_message=m.getMessage("error-files_selected_not_found"),
        options=options,
        colors=INPUT_THEME["ADD_SELECTION"],
        icons=INPUT_ICONS,
    )

    if len(answers) == 0:
        return m.log("error-files_selected_not_found")

    choices = []
    for answer in answers:
        choices.append(removeColors(answer))

    run(["git", "add"] + choices)
    m.log("add-success")


def addAll(fileSearch):
    from .Helpers import run, MessageControl
    from .Status import get_status, search_in_status

    m = MessageControl()
    status = get_status()

    if len(fileSearch) > 0:
        matches = search_in_status(fileSearch, status, excluded_files=["branch", "added"])

        return (
            m.log("error-file_match_not_found")
            if len(matches) == 0
            else add(matches, should_verify=False, messages=m)
        )

    has_files_to_add = False
    for status_id in status:
        if status_id == "branch" or status_id == "added":
            continue

        has_files_to_add = True
        break

    if has_files_to_add:
        run(["git", "add", "."])
        m.log("add-all-success")
    else:
        m.log("error-add-files_not_found")


def router(argument_manager, sub_route):
    if sub_route == "ADD_ALL":
        addAll(argument_manager.left_keys[1:])
    if sub_route == "DEFAULT":
        add(argument_manager.left_keys)
