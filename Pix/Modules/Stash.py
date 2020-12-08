def add_to_stash():
    from .Prompts import text
    from .Helpers import run, MessageControl
    from .Status import get_status
    from .Add import add
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()

    status = get_status()

    if len(status) == 1:
        return m.log("error-stash-addedfiles")

    if "conflicted" in status:
        return print("Error: There is conflicted files!")

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
        display_name = (
            m.get_message(
                "stash-list_item",
                {
                    "pm_stashname": name,
                    "pm_stashbranch": branch,
                },
            ),
        )

        stash_list.append(
            {"value": stash_id, "id": stash_id, "display_name": display_name}
        )

    print()
    stash_selected = multi_select(
        title=m.get_message("branch-selection-title"),
        options=stash_list,
        error_message=m.get_message("operation-cancel"),
        colors=INPUT_THEME["STASH_SELECTION"],
        icons=INPUT_ICONS,
    )

    if stash_selected == "":
        return m.log("error-empty")

    stash_id = stash_selected[0]
    run(["git", "stash", "pop", stash_id])
    m.log("stash-back-success", {"pm_stash": stash_selected})


def router(argument_manager, sub_route):
    if sub_route == "ADD_STASH":
        add_to_stash()
    if sub_route == "DEFAULT":
        stash_selection()
