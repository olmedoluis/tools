def get_common_directory(directories):
    from os.path import basename
    from os import getcwd

    directories_splitted = []
    for directory in directories:
        directories_splitted.append(directory.split("/"))

    if len(directories_splitted) == 1:
        return directories_splitted[0][-1]

    index = 0
    for example in directories_splitted[0]:
        for directory in directories_splitted:
            if example == directory[index]:
                continue

            return directory[index - 1] if index > 0 else basename(getcwd())

        index = index + 1

    return basename(getcwd())


def save():
    from .Prompts import many, confirm
    from .Status import get_status
    from .Helpers import run, MessageControl, removeColors
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS

    m = MessageControl()
    status = get_status()

    if not "added" in status:
        return m.log("error-commit-files_not_found")

    added_files = status["added"]

    m.log("added-title")
    for added_file in added_files:
        m.log("added", {"pm_change": added_file})

    options = ["feat", "refactor", "fix", "style"]
    scape_error = m.getMessage("operation-cancel")
    common_dir = get_common_directory(added_files)

    print()
    answers = many(
        [
            {
                "type": "select",
                "title": m.getMessage("commit-creation-type_title"),
                "options": options,
                "error_message": scape_error,
                "colors": INPUT_THEME["COMMIT_CREATION_TYPE"],
                "icons": INPUT_ICONS,
            },
            {
                "type": "text",
                "title": m.getMessage("commit-creation-scope_title"),
                "place_holder": removeColors(common_dir),
                "error_message": scape_error,
                "colors": INPUT_THEME["COMMIT_CREATION_SCOPE"],
            },
            {
                "type": "text",
                "title": m.getMessage("commit-creation-about_title"),
                "error_message": scape_error,
                "colors": INPUT_THEME["COMMIT_CREATION_ABOUT"],
            },
        ]
    )

    if len(answers) != 3:
        return m.log("error-empty")

    commit = "{}({}):{}".format(*answers)
    m.log("preview", {"pm_preview": commit})

    should_commit = confirm(
        title=m.getMessage("confirmation"),
        colors=INPUT_THEME["COMMIT_CREATION_CONFIRM"],
    )

    if should_commit:
        run(["git", "commit", "-m", commit])
        m.log("commit-success")
    else:
        m.log("commit-cancel")


def router(argument_manager, sub_route):
    if sub_route == "DEFAULT":
        save()
