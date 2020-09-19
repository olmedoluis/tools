def get_status_paths(status, excluded_files=[], included_files=[]):
    file_paths = []

    for status_id in status:
        status_content = status[status_id]

        if not (status_id in excluded_files) or status_id in included_files:
            file_paths = file_paths + status_content

    return file_paths


def add(file_paths=[], should_verify=True, messages=""):
    from .Prompts import multi_select
    from .Helpers import run, removeColors, MessageControl
    from .Status import get_status, search_in_status
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl() if messages == "" else messages
    status = get_status()

    file_paths = (
        search_in_status(file_paths, status, excluded_files=["branch", "added"])
        if len(file_paths)
        else get_status_paths(status, excluded_files=["branch", "added"])
    )

    if len(file_paths) == 0:
        return m.log("error-add-files_not_found")
    elif not should_verify:
        run(["git", "add"] + file_paths)
        return m.log("add-all-success")

    print()
    answers = multi_select(
        title=m.getMessage("add-title"),
        final_title=m.getMessage("file-selection-finaltitle"),
        error_message=m.getMessage("error-files_selected_not_found"),
        options=file_paths,
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


def add_all():
    add(file_paths=[], should_verify=False)


def router(argument_manager, sub_route):
    if sub_route == "ADD_ALL":
        add_all()
    if sub_route == "DEFAULT":
        add(argument_manager.left_keys)
