import os

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
        self.tabs.setStyleSheet("QTabBar::tab { height: 60px; width: 70px; }")
        self.tabs.setIconSize( QtCore.QSize(50, 50) )
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
    
    def addNewTab(self, layout, tab_name, icons_path=False):
        newTab = QWidget()
        newTab.setLayout(layout)
        self.tabs.addTab(newTab, tab_name)
        
        icon = False
        if icons_path:
            img = f"{icons_path}/{tab_name}.png"
            if os.path.exists(img):
                icon = QtGui.QIcon(img)
                #newTab.setIconSize( QtCore.QSize(self.iconSize, self.iconSize) )
            else:
                pass
        
        if icon:
            self.tabs.addTab(newTab, icon, tab_name)
        else:
            self.tabs.addTab(newTab, tab_name)

