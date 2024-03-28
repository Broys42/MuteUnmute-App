from typing import List
from pycaw.pycaw import AudioUtilities, AudioSession
from UserSettings import UserSettings

class AudioSource():
      def __init__(self, AudioSession : AudioSession) -> None:
          self.pid = AudioSession.Process.pid
          self.name = AudioSession.Process.name()

class AudioSourcesMaker():
    def __init__(self) -> None:
        self.audioSoursesList = []
        self.sessions : List[AudioSession] = []

    def makeAudioSourcesList(self) -> List:
        self.audioSoursesList.clear()
        self.sessions.clear()
        self.sessions = AudioUtilities.GetAllSessions()

        for session in self.sessions:
            if session.Process and session.Process.name() != "System Sounds":
                self.audioSoursesList.append(AudioSource(session))

        return self.audioSoursesList

class MuteSwitcher():
    def __init__(self, userSettings: UserSettings) -> None:
        self.userSettings = userSettings
        self.sessions : List[AudioSession] = []

    def switchMuteStatus(self):
        self.sessions.clear()
        self.sessions : List[AudioSession] = AudioUtilities.GetAllSessions()

        for session in self.sessions:
            volume = session.SimpleAudioVolume
            if session.Process and session.Process.name() != "System Sounds":
                if session.Process.pid == self.userSettings.audioSourcePID:
                    if volume.GetMute() == 1:
                        print("Mute")
                        volume.SetMute(0, None)
                    else:
                        print("Unmute")
                        volume.SetMute(1, None)
