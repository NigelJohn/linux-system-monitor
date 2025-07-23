from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QTimer
import json
from .collector import collect_metrics
import sys
import os

class MonitorWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Monitor")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)  # Update every second

        # Set size and position
        self.setFixedSize(160, 160)
        self.move(1700, 30)  # Adjust for your screen

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        # Image button
        self.button = QtWidgets.QPushButton()
        icon_path = os.path.abspath("linux-system-monitor\res\amaterasu.png")  # Replace with your actual PNG path
        icon = QtGui.QIcon(icon_path)
        self.button.setIcon(icon)
        self.button.setIconSize(QtCore.QSize(64, 64))
        self.button.setFixedSize(72, 72)
        self.button.setStyleSheet("border: none;")

        layout.addWidget(self.button, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        # Text area (optional for now)
        self.text = QtWidgets.QPlainTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        # Connections
        self.button.clicked.connect(self.toggle_metrics)

        # Timer for updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_metrics)

    def toggle_metrics(self):
        if self.timer.isActive():
            self.timer.stop()
            self.text.setPlainText("")
            self.setFixedSize(160, 160)
        else:
            self.timer.start(1000)
            self.setFixedSize(400, 500)  

    def update_metrics(self):
        metrics = collect_metrics()
        print(metrics)  # Debug output
        pretty_json = json.dumps(metrics, indent=2)
        self.text.setPlainText(pretty_json)



def start_ui():
    app = QtWidgets.QApplication(sys.argv)
    widget = MonitorWidget()
    widget.show()
    sys.exit(app.exec())