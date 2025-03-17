import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import subprocess

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 com Dashboard Dash")

        # Layout principal
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Widget QWebEngineView para carregar o dashboard
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8050"))  # URL do Dashboard
        layout.addWidget(self.browser)

        # Inicializar o servidor Dash
        self.start_dashboard_server()

    def start_dashboard_server(self):
        # Subprocesso para rodar o servidor do Dash
        subprocess.Popen(["python", "dashboard.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec_())
