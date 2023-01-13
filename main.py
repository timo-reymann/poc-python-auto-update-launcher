import sys
import time
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QProgressBar, QErrorMessage, QMessageBox

from update import fetch_current_version, retrieve_installed_version, update_app, launch_app


class UpdateThread(QThread):
    update_ui_text = Signal(str)
    update_result = Signal(bool)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.existing = True

    def run(self):
        installed_version = retrieve_installed_version()

        try:
            current_version = fetch_current_version()
            self.update_ui_text.emit("Current version installed: %s ..." % current_version)

            if installed_version != current_version:
                self.update_ui_text.emit("Update version to %s ..." % current_version)
            update_app(current_version)
        except Exception as e:
            cause = str(e)
            if installed_version is None:
                self.update_ui_text.emit(
                    "Could not load newest version from server and no version found locally\nError message: %s" % cause)
                self.update_result.emit(False)
                return
            else:
                self.update_ui_text.emit("Starting last offline version")

        if installed_version is None:
            installed_version = current_version

        self.update_ui_text.emit("Starting application in version %s ..." % installed_version)
        launch_app()
        self.update_result.emit(True)


class UpdateDialog(QWidget):
    update_result = None

    def __init__(self):
        QWidget.__init__(self)
        self.resize(300, 100)

        self.progress_bar = QProgressBar(minimum=0, maximum=0)
        self.message = QLabel("Launching your application")
        self.message.alignment = Qt.AlignCenter
        self.setWindowTitle("Launcher")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.message)

        self.thread = UpdateThread(self)
        self.thread.update_ui_text.connect(self.update_ui_text)
        self.thread.update_result.connect(self.set_update_result)
        self.thread.finished.connect(self.exit_app)
        self.thread.start()

    def set_update_result(self, result):
        self.update_result = result

    def exit_app(self):
        if self.update_result:
            self.close()
            return

        msg = QMessageBox(self)
        msg.setWindowTitle("Failed to launch")
        msg.setWindowModality(Qt.WindowModal)
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Failed to update and launch application.\n\n" +
                    self.message.text())
        self.close()
        msg.exec_()

    def update_ui_text(self, text: str) -> None:
        print(text)
        self.message.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = UpdateDialog()
    dialog.show()
    sys.exit(app.exec_())
