import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import os

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-logging" 
app=QApplication(sys.argv)

class PageLoader(QWebEnginePage):
    def __init__(self, uri):
        self.app = app
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(uri))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

