import sys

from View import UIImporter, UIConfigurator

from PyQt6.QtWidgets import QApplication

from ViewModel import ViewModel


class Model():
    def __init__(self) -> None:
        self.viewModel = ViewModel()

def main():
    model = Model()
    openWindow(model)

def openWindow(model: Model):
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = UIImporter("MuteUnmuteUI.ui")
        configurator = UIConfigurator(window, model.viewModel)
        window.show()
        sys.exit(app.exec())

main()
