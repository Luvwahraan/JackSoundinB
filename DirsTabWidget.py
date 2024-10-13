import os

from PyQt5 import QtGui
from PyQt5 import QtCore

from PyQt5.QtWidgets import QWidget, QTabWidget, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

class DirsTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        # jack channels status
        self.statusBox = QVBoxLayout()
        self.statusTitles = []
        self.statusLabels = []
        self.layout.addLayout(self.statusBox)

        # Soundboard dirs
        self.tabs = QTabWidget(self)
        #self.tabs.setTabPosition(QTabWidget.East)
        self.tabs.setStyleSheet("QTabBar::tab { height: 60px; width: 70px; }")
        self.tabs.setIconSize( QtCore.QSize(50, 50) )
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def addChannel(self, channel_nb):
        # title, formatted
        #label.setTextFormat(QtCore.Qt.RichText)
        title = QLabel(f"Channel {channel_nb}")
        title.setStyleSheet('color: darkgreen; font-size: 1.2em;')
        self.statusTitles.append(title)

        # status, raw
        statusLabel = QLabel('')
        
        self.statusBox.addWidget( self.statusTitles[channel_nb] )
        self.statusLabels.append(statusLabel)
        self.statusBox.addWidget( self.statusLabels[channel_nb] )

    def fillChannel(self, channel_nb, text='full'):
        self.statusLabels[channel_nb].setText(f"{text}")
        self.statusTitles[channel_nb].setStyleSheet('color: red; font-size: 1.2em;')
    def freeChannel(self, channel_nb, text=''):
        self.fillChannel(channel_nb, f"{text}")
        self.statusTitles[channel_nb].setStyleSheet('color: darkgreen; font-size: 1.2em;')
    
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

