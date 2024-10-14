import os

from PyQt5 import QtGui
from PyQt5 import QtCore

from PyQt5.QtWidgets import QWidget, QTabWidget, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

class DirsTabWidget(QWidget):
    def __init__(self, parent, max_queue):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        # jack channels status
        self.statusBox = QVBoxLayout()
        self.statusBox.setSpacing(0)
        self.statusBox.setContentsMargins(0, 0, 0, 0)
        self.statusTitles = []
        self.statusLabels = []
        self.layout.addLayout(self.statusBox)
        self.titleStyle = 'font-size: 16px; margin: 0; padding: 0;'
        self.labelStyle = 'color: darkblue; margin: 0; padding: 0;'
        
        # Label for soundfiles in queue
        self.maxQueue = max_queue
        self.soundList = []
        for i in range(0, self.maxQueue):
            self.soundList.append('')
        self.soundListLabel = QLabel()
        self.updateSoundListLabel()
        self.soundListTitle = QLabel('Queue')
        self.soundListTitle.setStyleSheet(f"color: darkgreen; {self.titleStyle}")
        self.statusBox.addWidget(self.soundListTitle, \
                alignment=QtCore.Qt.AlignBottom )
        self.statusBox.addWidget(self.soundListLabel, \
                alignment=QtCore.Qt.AlignBottom )

        # Soundboard dirs
        self.tabs = QTabWidget(self)
        #self.tabs.setTabPosition(QTabWidget.East)
        self.tabs.setStyleSheet("QTabBar::tab { height: 60px; width: 70px; }")
        self.tabs.setIconSize( QtCore.QSize(50, 50) )
        self.layout.addWidget(self.tabs)
        
        self.setLayout(self.layout)

    def updateSoundListLabel(self):
        # Complete list with empty text
        for i in range( len(self.soundList), self.maxQueue ):
            self.soundList.insert(0, '')

        # We want empty text top
        self.soundList.sort()
        
        # Transforms list in text and shows it
        labelText = "\n".join(self.soundList)
        self.soundListLabel.setText( labelText )

    def addSoundInQueue(self, soundname):
        self.soundList.remove('')
        self.soundList.append(soundname)
        self.updateSoundListLabel()
        
        if len(self.soundList) - self.soundList.count('') >= self.maxQueue:
            self.soundListTitle.setStyleSheet(f"color: red; {self.titleStyle}")
        else:
            self.soundListTitle.setStyleSheet(f"color: darkgreen; {self.titleStyle}")
        
        return len( self.soundList )

    def removeSoundInQueue(self, soundname):
        try:
            self.soundList.remove(soundname)
            self.updateSoundListLabel()
        except ValueError:
            pass
        
        if len(self.soundList) - self.soundList.count('') >= self.maxQueue:
            self.soundListTitle.setStyleSheet(f"color: red; {self.titleStyle}")
        else:
            self.soundListTitle.setStyleSheet(f"color: darkgreen; {self.titleStyle}")

    def addChannel(self, channel_nb):
        # title, formatted
        #label.setTextFormat(QtCore.Qt.RichText)
        title = QLabel(f"Channel {channel_nb}")
        title.setStyleSheet(f"color: darkgreen; {self.titleStyle}")
        title.setFixedWidth(150)
        self.statusTitles.append(title)

        # status, raw
        statusLabel = QLabel('')
        
        self.statusBox.insertWidget(0, self.statusTitles[channel_nb], \
                alignment=QtCore.Qt.AlignTop )
        self.statusLabels.append(statusLabel)
        self.statusBox.insertWidget(1, self.statusLabels[channel_nb], \
                alignment=QtCore.Qt.AlignTop )

    def fillChannel(self, channel_nb, text='full'):
        self.statusLabels[channel_nb].setText(f"{text}")
        self.statusTitles[channel_nb].setStyleSheet( \
                f"color: red; {self.titleStyle}")
        self.statusLabels[channel_nb].setStyleSheet( self.labelStyle )

    def freeChannel(self, channel_nb, text=''):
        self.fillChannel(channel_nb, f"{text}")
        self.statusTitles[channel_nb].setStyleSheet( \
                f"color: darkgreen; {self.titleStyle}")
    
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

