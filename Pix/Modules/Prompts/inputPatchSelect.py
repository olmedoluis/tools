def patch_select(error_message="", files=[], colors={}, icons={}):
    from .Console import ConsoleControl, getGetch
    from .CharactersInterpreter import get_parsed_char

    getch = getGetch()
    input_console = ConsoleControl(lines="default")
    patch_control = PatchControl(
        offset=0,
        term_size_x=input_console.terminalWidth,
        term_size_y=input_console.terminalHeight,
        files=files,
        colors=colors,
        icons=icons,
        keywords={"+": "modification", "-": "deletation"},
    )

    patch_control.set_patches_of_file(1)
    patch_control.set_patch_showing(0)

    while True:
        input_console.setConsoleLine(1, 2, patch_control.get_file_index_shown())
        input_console.setConsoleLine(3, 1, patch_control.get_current_file_name())

        for line_number in range(5, input_console.terminalHeight):
            text_to_show = patch_control.get_styled_patch_line(line_number)

            input_console.setConsoleLine(line_number, 1, text_to_show)

        input_console.refresh()

        char = getch()
        state = get_parsed_char(char)

        if state == "S":
            patch_control.increase_offset()
        elif state == "W":
            patch_control.decrease_offset()
        elif state == "D":
            patch_control.change_patch_page(1)
        elif state == "A":
            patch_control.change_patch_page(-1)
        elif state == "E":
            patch_control.change_selected_patch_state(transition="add")
        elif state == "Q":
            patch_control.change_selected_patch_state(transition="remove")
        elif state == "Y":
            patch_control.change_selected_patch_state(
                transition="add", force_transition=True
            )
            patch_control.change_patch_page(1)
        elif state == "N":
            patch_control.change_selected_patch_state(
                transition="remove", force_transition=True
            )
            patch_control.change_file_page(1)
        elif state == "FINISH":
            break
        elif state == "BREAK_CHAR":
            input_console.deleteLastLines(input_console.terminalHeight + 4)
            input_console.finish()
            print(error_message)
            exit()

    input_console.deleteLastLines(input_console.terminalHeight + 4)
    input_console.finish()

    return patch_control.files


class PatchControl:
    def __init__(
        self, offset, term_size_x, term_size_y, files, colors, icons, keywords
    ):
        from .Theme import INPUT_THEME, INPUT_ICONS

        self._KEYWORDS = keywords
        self._ICONS = {**INPUT_ICONS, **icons}
        self._COLORS = {**INPUT_THEME, **colors}
        self._RESET = self._COLORS["reset"]
        self._state_color = self._COLORS["border"]
        self._patches = []
        self._offset = offset
        self._term_size_x = term_size_x
        self._term_size_y = term_size_y
        self._patch_index_selected = 0
        self._patch_showing = []
        self._text_zone_area = range(0)
        self._file_name_index = 0
        self.files = files

    def set_patches_of_file(self, times):
        self._patches = self.files[self._file_name_index].patches
        self._patch_index_selected = 0 if times > 0 else len(self._patches) - 1

    def set_patch_showing(self, index):
        self._patch_showing = self._patches[index][1:]
        self._text_zone_area = range(0, len(self._patch_showing))

    def decrease_offset(self):
        newOffset = self._offset - 1
        self._offset = newOffset if newOffset in self._text_zone_area else self._offset

    def increase_offset(self):
        newOffset = self._offset + 1
        self._offset = (
            newOffset
            if newOffset in self._text_zone_area
            and (len(self._patch_showing) > self._term_size_y)
            and (newOffset < (len(self._patch_showing) * 0.5))
            else self._offset
        )

    def _update_state_color(self):
        is_patch_selected = self.get_is_patch_selected()

        if is_patch_selected:
            self._state_color = self._COLORS["borderSel"]

            return

        self._state_color = (
            self._COLORS["deletation"]
            if self._get_current_file().is_file_removed
            else self._COLORS["border"]
        )

    def change_file_page(self, times):
        self._file_name_index = (self._file_name_index + times) % len(self.files)
        self.set_patches_of_file(times)
        self._update_state_color()

    def change_patch_page(self, times):
        newIndex = self._patch_index_selected + times
        self._patch_index_selected = newIndex % len(self._patches)

        if not (newIndex in range(len(self._patches))) and len(self.files) > 1:
            self.change_file_page(times)

        self.set_patch_showing(self._patch_index_selected)
        self._offset = 0
        self._update_state_color()

    def _get_current_file(self):
        return self.files[self._file_name_index]

    def add_index_selected_to_patch(self):
        if not self.get_is_patch_selected():
            self._get_current_file().patches_selected_add.append(
                self._patch_index_selected
            )

            self._update_state_color()

    def remove_index_selected_to_patch(self):
        patch_indexes = self._get_current_file().patches_selected_add
        hasRemoved = False

        if self.get_is_patch_selected():
            self._get_current_file().patches_selected_add.remove(
                self._patch_index_selected
            )

            self._update_state_color()
            hasRemoved = True

        return hasRemoved

    def change_selected_patch_state(self, transition, force_transition=False):
        current_file = self._get_current_file()

        if transition == "remove":
            has_removed_from_added = self.remove_index_selected_to_patch()

            if not has_removed_from_added or force_transition:
                current_file.is_file_removed = True

        elif transition == "add":
            was_file_removed = current_file.is_file_removed
            current_file.is_file_removed = False

            if not was_file_removed or force_transition:
                if self.get_is_patch_selected():
                    self.add_patches()
                else:
                    self.add_index_selected_to_patch()

        self._update_state_color()

    def add_patches(self):
        current_file = self._get_current_file()

        for index in range(len(self._patches)):
            if not (index in current_file.patches_selected_add):
                current_file.patches_selected_add.append(index)

    def get_styled_patch_line(self, lineNumber):
        index = lineNumber + self._offset - 5
        lineText = (
            self._patch_showing[index][0 : self._term_size_x - 5]
            if index in self._text_zone_area
            else ""
        )

        if len(lineText):
            firstChar = lineText[0]
            icon = self._ICONS[firstChar] if firstChar in self._ICONS else firstChar
            color = (
                self._COLORS[self._KEYWORDS[firstChar]]
                if firstChar in self._KEYWORDS
                else self._COLORS["slight"]
            )

            lineText = color + icon + lineText[1:] + self._RESET

        return f"{self._state_color}❚{self._RESET}   {lineText}"

    def get_is_patch_selected(self):
        return (
            self._patch_index_selected in self._get_current_file().patches_selected_add
        )

    def get_current_file_name(self):
        return self.files[self._file_name_index].file_name

    def get_patch_index_shown(self):
        output = ""

        for index in range(0, len(self._patches)):
            active = (
                self._COLORS["selection"] if index == self._patch_index_selected else ""
            )
            color = self._COLORS["index"]
            icon = self._ICONS["normal"]
            patch = self.files[self._file_name_index]

            if index in patch.patches_selected_add:
                color = self._COLORS["indexSel"]
                icon = self._ICONS["selection"]
            elif patch.is_file_removed:
                color = self._COLORS["deletation"]
                icon = self._ICONS["-"]

            output = f"{output}{color}{active} {icon}{self._RESET}"

        return f"{output} "

    def get_file_index_shown(self):
        output = ""

        for index in range(0, len(self.files)):
            color = self._COLORS["file"]
            extra = ""

            if index == self._file_name_index:
                color = self._COLORS["fileAct"]
                extra = self.get_patch_index_shown()

            output = f"{output}{color}|{self._RESET}{extra}"

        return output
