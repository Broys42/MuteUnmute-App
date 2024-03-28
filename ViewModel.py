
from AudioSource import AudioSourcesMaker
from AudioSource import AudioSource
from AudioSource import MuteSwitcher

from KeySequenceSetup import KeySequenceSetup
from UserSettings import UserSettings

from typing import List

class ViewModel():
    def __init__(self) -> None:
        self.userSettings = UserSettings()
        self.audioSource = AudioSourcesMaker()
        self.audioSources : List[AudioSource] = []
        self.keySequenceSetup = KeySequenceSetup(self.userSettings)
        self.muteSwitcher = MuteSwitcher(self.userSettings)

    def fillAudioSoursesList(self):
        self.audioSources.clear()
        self.audioSources = self.audioSource.makeAudioSourcesList()
