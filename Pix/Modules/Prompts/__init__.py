from .InputText import text
from .InputSelect import select
from .InputConfirm import confirm
from .InputMultiSelect import multi_select
from .inputPatchSelect import patch_select


def many(selectedInputsData):
    STORE = {
        "text": text,
        "select": select,
        "confirm": confirm,
        "multi_select": multi_select,
        "patch_select": patch_select,
    }
    responses = []

    for selectedInputData in selectedInputsData:
        selectedInput = STORE[selectedInputData["type"]]
        selectedInputData.pop("type")
        response = selectedInput(**selectedInputData)

        if response == "":
            break

        responses.append(response)

    return responses
