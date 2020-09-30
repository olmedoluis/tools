def add_to_file(text, file_path):
    f = open(file_path, "w+")
    f.write(text)
    f.close()


def parse_patch(indexes, meta_data, carried_values, values):
    if len(indexes):
        carried_values = carried_values + meta_data

        for index in indexes:
            carried_values = carried_values + values[index]

    return carried_values


def set_last_space(patches):
    if not len(patches):
        patches = [""]

    return patches if patches[-1] == "" else patches + [""]


def parse_files(files):
    parsed_patches_add = []
    files_to_remove = []

    for file in files:
        if file.is_file_removed:
            files_to_remove = files_to_remove + [file.file_name_raw]
            continue

        parsed_patches_add = parse_patch(
            indexes=file.patches_selected_add,
            meta_data=file.meta_data,
            carried_values=parsed_patches_add,
            values=file.patches,
        )

    return set_last_space(parsed_patches_add), files_to_remove


def parse_differences(differences_raw, files, get_message):
    class File:
        def __init__(self, file_name, file_name_raw, meta_data):
            self.file_name = file_name
            self.file_name_raw = file_name_raw
            self.meta_data = meta_data
            self.patches = []
            self.patches_selected_add = []
            self.is_file_removed = []

    lines = differences_raw.split("\n")
    differences = []

    index = 0
    last_index = 0
    for line in lines[1:]:
        if "diff --git a" == line[:12]:
            differences.append(lines[last_index : index + 1])
            last_index = index + 1

        index = index + 1

    differences.append(lines[last_index:])

    output_patches = []
    index_file = 0
    for lines in differences:
        meta_data = lines[:4]
        new_patch = File(
            file_name=get_message("file-title", {"pm_file": files[index_file]}),
            file_name_raw=files[index_file],
            meta_data=meta_data,
        )

        index = 4
        last_index = 4
        for line in lines[5:]:
            if "@@ " == line[:3] and " @@" in line[3:]:
                new_patch.patches.append(lines[last_index : index + 1])
                last_index = index + 1

            index = index + 1

        last_patch = lines[last_index:]
        new_patch.patches.append(
            last_patch[:-1] if last_patch[-1] == "" else last_patch
        )
        output_patches.append(new_patch)
        index_file = index_file + 1

    return output_patches


def patch(files, messages=""):
    from .Prompts import patch_select
    from .Helpers import run, MessageControl
    from Configuration.Theme import INPUT_THEME, INPUT_ICONS
    from pathlib import Path

    m = MessageControl() if messages == "" else messages

    cwd = Path.cwd()
    file_path = f"{cwd}/changes.patch"

    differences_raw = run(["git", "diff-files", "-p"] + files)
    patches = parse_differences(differences_raw, files, m.getMessage)

    selected_patches = patch_select(
        files=patches,
        error_message=m.getMessage("error-files_selected_not_found"),
        colors=INPUT_THEME["PATCH_SELECTION"],
        icons=INPUT_ICONS,
    )

    patch_generated_add, patch_generated_remove = parse_files(selected_patches)

    if len(patch_generated_add) != 1:
        # add_to_file("\n".join(patch_generated_add), file_path)
        # run(["git", "apply", "--cached", file_path])
        pass

    if len(patch_generated_remove) != 1:
        # add_to_file("\n".join(patch_generated_remove), file_path)
        # run(["git", "checkout", "--patch", file_path])
        pass

    if len(patch_generated_remove) != 1 and len(patch_generated_add) != 1:
        return m.log("error-empty")

    # run(["rm", file_path])
    m.log("patch-success")


def patch_all(file_search):
    from .Status import get_status, search_in_status
    from .Helpers import MessageControl

    m = MessageControl()

    status = get_status()
    if len(file_search) > 0:
        matches = search_in_status(file_search, status, included_files=["modified"])

        return (
            m.log("error-file_match_not_found")
            if len(matches) == 0
            else patch(matches, m)
        )

    files = status["modified"] if "modified" in status else []

    if not len(files):
        return m.log("error-patch-files-not-found")

    patch(files)


def router(argument_manager, sub_route):
    if sub_route == "DEFAULT":
        patch_all(argument_manager.left_keys)
