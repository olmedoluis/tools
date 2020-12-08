def add_to_stash():
    from .Prompts import text
    from .Helpers import run, MessageControl
    from .Status import get_status
    from .Add import add
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()

    status = get_status()

    if len(status) == 1:
        return m.log("error-stash-files_not_found")

    if "conflicted" in status:
        return m.log("error-stash_in_conflicted")

    if not "added" in status or len(status) > 2:
        add(use_availables=True)

    print()
    title = text(
        title=m.get_message("stash-in-title"),
        error_message=m.get_message("operation-cancel"),
        colors=INPUT_THEME["STASH_CREATION_NAME"],
    )

    if title == "":
        return m.log("error-empty")

    run(["git", "stash", "push", "-m", title])
    m.log("stash-in-success")


def stash_selection():
    from .Prompts import multi_select
    from .Helpers import run, MessageControl
    from .Status import get_status
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()

    stashes_raw = run(["git", "stash", "list"])
    stashes_spaced = stashes_raw.rstrip().split("\n")

    if stashes_spaced[0] == "":
        return m.log("error-stash-stashes_not_found")

    stash_list = []
    for stash_with_spaces in stashes_spaced:
        stash = stash_with_spaces.lstrip()

        id_start_index = stash.find("{") + 1
        stash_id = stash[id_start_index : id_start_index + 1]

        branch_start_index = stash.find("On") + 3
        branch_end_index = stash.find(" ", branch_start_index) - 1
        branch = stash[branch_start_index:branch_end_index]

        name = stash[branch_end_index + 2 :]
        display_name = m.get_message(
            "stash-list_item",
            {
                "pm_stashname": name,
                "pm_stashbranch": branch,
            },
        )

        stash_list.append(
            {"value": stash_id, "id": stash_id, "display_name": display_name}
        )

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

    for stash_id in stashes_selected:
        run(["git", "stash", "apply", "stash@{" + stash_id + "}"])

    stashes_selected_from_list = []
    for stash_id in stashes_selected:
        for stash in stash_list:
            if stash["id"] == stash_id:
                stashes_selected_from_list.append(stash["display_name"])

    m.log("stash-back-success")
    m.logMany(
        message_id="stash-name",
        param_name="pm_name",
        contents=stashes_selected_from_list,
    )


def router(argument_manager, sub_route):
    if sub_route == "ADD_STASH":
        add_to_stash()
    if sub_route == "DEFAULT":
        stash_selection()
