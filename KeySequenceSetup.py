from PyQt6.QtWidgets import QKeySequenceEdit
from UserSettings import UserSettings

class KeySequenceSetup():
    def __init__(self, userSettings: UserSettings) -> None:
        self.userSettings = userSettings

    def setKeySequenceToUserSettings(self, keySequenceEdit: QKeySequenceEdit):
        keySequence = keySequenceEdit.keySequence()
        keySequenceStr = keySequence.toString()

        print(f"Нажата комбинация {keySequenceStr}")

        if keySequenceStr.__contains__("Ctrl") or keySequenceStr.__contains__("Alt"):
            self.userSettings.shortCutChange(f"{keySequenceStr}")
            keySequenceEdit.clearFocus()
        else:
            self.userSettings.shortCutChange("")
            keySequenceEdit.clear()
            keySequenceEdit.clearFocus()
