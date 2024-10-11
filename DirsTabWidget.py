from PyQt5 import QtGui
from PyQt5 import QtCore

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QStatusBar

class DirsTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
    
    def addNewTab(self, layout, tab_name):
        newTab = QWidget()
        newTab.setLayout(layout)
        self.tabs.addTab(newTab, tab_name)
