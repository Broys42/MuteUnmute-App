class UserSettings():
    def __init__(self) -> None:
        self.shortCut = "";
        self.audioSourceName = "";
        self.audioSourcePID = 0;

    def shortCutChange(self, shortCut):
        self.shortCut = shortCut
