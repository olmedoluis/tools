def add_to_stash():
    from .Prompts import text
    from .Helpers import run, MessageControl
    from .Status import get_status
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()

    status = get_status()

    if not "added" in status:
        return m.log("error-stash-files_not_found")

    print()
    title = text(
        title=m.get_message("stash-in-title"),
        error_message=m.get_message("operation-cancel"),
        colors=INPUT_THEME["STASH_CREATION_NAME"],
    )

    if title == "":
        return m.log("error-empty")

    run(["git", "stash", "push", "-m", title, "--", *status["added"]])
    m.log("stash-in-success")


def get_stashes_list(messages, should_sort_list=False):
    from .Helpers import run

    stashes_raw = run(["git", "stash", "list"])
    stashes_spaced = stashes_raw.rstrip().split("\n")

    if stashes_spaced[0] == "":
        messages.log("error-stash-stashes_not_found")
        exit()

    stash_list = []

    for stash_with_spaces in stashes_spaced:
        stash = stash_with_spaces.lstrip()

        id_start_index = stash.find("{") + 1
        id_end_index = stash.find("}")
        stash_id = stash[id_start_index:id_end_index]

        branch_start_index = stash.find("On") + 3
        branch_end_index = stash.find(" ", branch_start_index) - 1
        branch = stash[branch_start_index:branch_end_index]

        name = stash[branch_end_index + 2 :]

        display_name = messages.get_message(
            "stash-list_item",
            {
                "pm_stashname": name,
                "pm_stashbranch": branch,
            },
        )

        stash_list.append(
            {"value": stash_id, "id": stash_id, "display_name": display_name}
        )

    if should_sort_list:
        stash_list.sort(key=lambda stash: stash["display_name"])

    return stash_list


def remove_stash():
    from .Prompts import multi_select
    from .Helpers import run, MessageControl
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()

    stash_list = get_stashes_list(messages=m)

    print()
    stashes_selected = multi_select(
        title=m.get_message("branch-selection-title"),
        options=stash_list,
        error_message=m.get_message("operation-cancel"),
        colors=INPUT_THEME["STASH_SELECTION"],
        icons=INPUT_ICONS,
    )

    if len(stashes_selected) == 0:
        return m.log("error-empty")

    stashes_selected.sort(reverse=True)

    m.log("stash-remove-success")
    for stash_id in stashes_selected:
        run(["git", "stash", "drop", "stash@{" + stash_id + "}"])

        stash_display_name = ""
        for stash in stash_list:
            if stash["id"] == stash_id:
                stash_display_name = stash["display_name"]
                break

        m.log("stash-name", {"pm_name": stash_display_name})

    print()


def stash_selection():
    from .Prompts import multi_select
    from .Helpers import run, MessageControl
    from .Status import get_status
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()

    stash_list = get_stashes_list(messages=m, should_sort_list=True)

    print()
    stashes_selected = multi_select(
        title=m.get_message("branch-selection-title"),
        options=stash_list,
        error_message=m.get_message("operation-cancel"),
        colors=INPUT_THEME["STASH_SELECTION"],
        icons=INPUT_ICONS,
    )

    if len(stashes_selected) == 0:
        return m.log("error-empty")

    show_success_title = True
    for stash_id in stashes_selected:
        run(["git", "stash", "apply", "stash@{" + stash_id + "}"])

        stash_display_name = ""
        for stash in stash_list:
            if stash["id"] == stash_id:
                stash_display_name = stash["display_name"]
                break

        if show_success_title:
            m.log("stash-back-success")

        m.log("stash-name", {"pm_name": stash_display_name})
        show_success_title = False

    print()


def router(argument_manager, sub_route):
    if sub_route == "ADD_STASH":
        add_to_stash()
    if sub_route == "REMOVE_STASH":
        remove_stash()
    if sub_route == "DEFAULT":
        stash_selection()
