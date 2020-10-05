from .InputText import text
from .InputSelect import select
from .InputConfirm import confirm
from .InputMultiSelect import multi_select
from .inputPatchSelect import patch_select
from .InputLog import logger


def many(selected_inputs_data):
    STORE = {
        "text": text,
        "select": select,
        "confirm": confirm,
        "multi_select": multi_select,
        "patch_select": patch_select,
        "logger": logger,
    }
    responses = []

    for selected_input_data in selected_inputs_data:
        selected_input = STORE[selected_input_data["type"]]
        selected_input_data.pop("type")
        response = selected_input(**selected_input_data)

        if response == "":
            break

        responses.append(response)

    return responses
