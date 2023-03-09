from enum import Enum


class GlobalErrorMessages(Enum):
    WRONG_STATUS_CODE = "Received status code doesn't match to expected."
    WRONG_NUMBER_OF_ELEMENTS = "Received number of elements doesn't match to expected."
