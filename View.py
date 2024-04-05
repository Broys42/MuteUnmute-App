import keyboard
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QKeySequenceEdit, QLabel, QComboBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QAction
from PyQt6.uic import loadUi

from typing import List

from AudioSource import AudioSource

from ViewModel import ViewModel

class UIImporter(QMainWindow):
    def __init__(self):
        super().__init__()
        currentdir = os.path.dirname(os.path.abspath(__file__))
        uipath = os.path.join(currentdir, "MuteUnmuteUI", "MuteUnmuteUI.ui")

        loadUi(uipath, self)

class UIConfigurator(QMainWindow):
    def __init__(self, window: QMainWindow, viewModel : ViewModel):
        super().__init__()
        self.window = window
        self.viewModel = viewModel
        self.audioSourceItemsModel : QStandardItemModel = QStandardItemModel()
        self.audioSourceItemsList : List[QStandardItemModel] = []

        self.action_muteSwitcher : QAction = QAction("MuteSwitcher", self)
        self.action_muteSwitcher.triggered.connect(self.muteSwitcherAction)

        self.window.addAction(self.action_muteSwitcher)

        #Declaration of interface element data types
        self.label : QLabel = self.window.label
        self.keySequenceEdit : QKeySequenceEdit = self.window.keySequenceEdit
        self.comboBoxOfAudioSources : QComboBox = self.window.comboBoxOfAudioSources

        self.label.adjustSize()

        self.keySequenceEdit.setMaximumSequenceLength(1)
        self.keySequenceEdit.editingFinished.connect(self.keySequenceEdititingFinished)

        self.fillComboBoxOfAudioSources()

        #When Click on ComboBox
        self.comboBoxOfAudioSources.mousePressEvent = self.comboBoxIsOpen

        #When Select Item in ComboBox
        self.comboBoxOfAudioSources.activated.connect(self.comboBoxOfAudioSourceActivated)

        self.comboBoxOfAudioSources.setCurrentIndex(-1)

    def muteSwitcherAction(self):
        self.viewModel.muteSwitcher.switchMuteStatus()

    def comboBoxIsOpen(self, event):
        self.comboBoxOfAudioSources.showPopup()
        self.comboBoxOfAudioSources.clear()
        self.fillComboBoxOfAudioSources()

    def fillComboBoxOfAudioSources(self):
        self.viewModel.fillAudioSoursesList()
        self.fillAudioSourceItemsList()
        self.fillAudioSourceItemsModel()

        self.comboBoxOfAudioSources.setModel(self.audioSourceItemsModel)

    def fillAudioSourceItemsList(self):
        self.audioSourceItemsList.clear()
        for audioSource in self.viewModel.audioSources:
            self.audioSourceItemsList.append(QStandardItem(audioSource.name))

    def fillAudioSourceItemsModel(self):
        self.audioSourceItemsModel.clear()
        for index, audioSourceItem in enumerate(self.audioSourceItemsList):
            audioSourceItem.setData(self.viewModel.audioSources[index], role=Qt.ItemDataRole.UserRole)
            self.audioSourceItemsModel.appendRow(audioSourceItem)
            self.comboBoxOfAudioSources.setCurrentIndex(-1)
            self.saveChosenAppAfterResetModel()

    def saveChosenAppAfterResetModel(self):
        for index in range(self.comboBoxOfAudioSources.count()):
            item_data = self.comboBoxOfAudioSources.itemData(index, role=Qt.ItemDataRole.UserRole)
            if isinstance(item_data, AudioSource):
                if self.viewModel.userSettings.audioSourcePID == item_data.pid:
                    self.comboBoxOfAudioSources.setCurrentIndex(index)
                print(f"Item at index {index}: {item_data.name} with pid {item_data.pid}")

    def comboBoxOfAudioSourceActivated(self):
        selected_item = self.comboBoxOfAudioSources.itemData(self.comboBoxOfAudioSources.currentIndex(), role=Qt.ItemDataRole.UserRole)

        if isinstance(selected_item, AudioSource):
            self.viewModel.userSettings.audioSourceName = selected_item.name
            self.viewModel.userSettings.audioSourcePID = selected_item.pid
            print(f"Selected item: {selected_item.name} with pid {selected_item.pid}")

    def keySequenceEdititingFinished(self):
        self.viewModel.keySequenceSetup.setKeySequenceToUserSettings(self.keySequenceEdit)

        if self.viewModel.userSettings.shortCut:
            keyboard.unhook_all()
            keyboard.add_hotkey(f"{self.viewModel.userSettings.shortCut}".lower(), self.action_muteSwitcher.trigger)
        else:
            keyboard.unhook_all()
