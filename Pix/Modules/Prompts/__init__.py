from .InputText import text
from .InputSelect import select
from .InputConfirm import confirm
from .InputMultiSelect import multiSelect


def many(choosenInputsData):
    inputs = {
        "Text": text,
        "Select": select,
        "Confirm": confirm,
        "MultiSelect": multiSelect,
    }
    responses = []

    for choosenInputData in choosenInputsData:
        choosenInput = inputs[choosenInputData["type"]]
        choosenInputData.pop("type")

        response = choosenInput(**choosenInputData)
        if response == "":
            break
        responses.append(response)

    return responses
