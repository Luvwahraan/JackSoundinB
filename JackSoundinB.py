#!/usr/bin/env python3

import os
import sys

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QRunnable, QObject, QThreadPool
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QToolBar, QStatusBar, QToolButton


from JackPlayer import *
from DirsTabWidget import *

        

#class Window(QWidget):
class MainWindow(QMainWindow):
    def __init__(self, sound_directory, max_players=4):
        super(MainWindow, self).__init__()
        self.setWindowTitle("JackSoundinB")
        
        self.width = 800
        self.setGeometry(2520, 1080, self.width, 500)
        #self.setIcon('icons/mix.png')
        
        self.iconSize = 80
        
        self.soundDirectory = sound_directory
        self.imgDirectory = os.path.join(self.soundDirectory, 'icons')
        
        # Jackd players, in threads.
        self.maxPlayers = max_players
        self.players = []
        self.pool = QThreadPool.globalInstance()
        
        
        self.tabWidget = DirsTabWidget(self)
        
        # jack channels status
        for i in range(0, self.maxPlayers):
            self.tabWidget.addChannel(i)
        
        self.walkInSoundBank(self.soundDirectory)
        
        self.setCentralWidget(self.tabWidget)
        
        self.show()
    
    
    
    """
    Lists everything in soundbank directory except icons one, and
    assume that all are sound files.
    Each fil list is sent to generateButtons() method.
    """
    def walkInSoundBank(self, directory, layout='grid'):
        assert os.path.isdir(directory)
        
        files = os.scandir(directory)
        dirs = []
        soundfiles = []
        for entry in files:
            if entry.is_dir():
                #print(f"Dir {entry.name}")
                if entry.name != 'icons':
                    dirs.append(entry.name)
            else:
                #print(f"File {entry.name}")
                soundfiles.append(entry.name)
        
        if len(soundfiles) > 0:
            #print(f"({directory}, {soundfiles}, {directory})")
            self.generateButtons(directory, soundfiles, layout)
        
        if dirs :
            #print(f"Processing dirs: {dirs}")
            for new_dir in dirs:
                self.walkInSoundBank( os.path.join(directory, new_dir), new_dir )
        
        files.close()

        
    """
    Create a grid layout filled with on button per file in a directory, then
    add it in tab widget.
    If an png with file's name exists, assign that image to button.
    """
    def generateButtons(self, current_path, filenames, layout):
        #coord = { 'grid': [0, 0] }
        maxCol = 0
        row = 0
       
        #print(f"Creating layout {layout}")
        grid = QGridLayout()
        
        maxCol = int( self.width / ( self.iconSize + 15 ) )
        
        #print(f"Generating button for directory\n  {current_path}")
        row = 0
        column = 0
        for sf in filenames:
            filename,ext = os.path.splitext( sf )
            soundfile = os.path.join(current_path, sf)
            #print(f"\tbutton {filename}")
            
            #print("\tCreating button")
            button = QToolButton()
            
            #print("\tChecking icon")
            img = os.path.join( self.imgDirectory, f"{filename}.png" )
            if not os.path.exists(img):
                img = os.path.join( self.imgDirectory, 'clear.png' )
                
            button.setIcon( QtGui.QIcon(img) )
            button.setIconSize( QtCore.QSize(self.iconSize, self.iconSize) )
            #button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect( self.playSoundSignal(soundfile) )
            button.setToolTip( filename )
            
            #print(f"\tAdd to layout '{layout}'")
            grid.addWidget(button, row, column)
            #print(f"{maxCol} grid.addWidget(button, {row}, {column})")

            # Adapt grid to window width
            column += 1
            if column >= maxCol:
                column = 0
                row += 1
        
        # Complete last column by empty buttons
        if column < maxCol:
            img = os.path.join( self.imgDirectory, 'empty.png' )
            for i in range(column, maxCol):
                button = QToolButton()
                button.setIcon( QtGui.QIcon(img) )
                button.setIconSize( QtCore.QSize(self.iconSize, self.iconSize) )
                grid.addWidget(button)
                pass
            
            
        self.tabWidget.addNewTab( grid, layout, self.imgDirectory )
        
    """
    Threads handles
    """
    def startedPlayer(self, n):
        print(f"Started player {n}")
        self.players.append(n)
        self.tabWidget.fillChannel(n)
    def finishedPlayer(self, n):
        print(f"Finished player {n}")
        self.players.remove(n)
        self.tabWidget.freeChannel(n)
    
    def playSoundSignal(self, soundfile):
        def playSound():
            nextPlayer = len(self.players)
            if nextPlayer < self.maxPlayers:
                player = JackPlayer(nextPlayer, soundfile)
                player.signals.started.connect(self.startedPlayer)
                player.signals.completed.connect(self.finishedPlayer)
                self.pool.start(player)
            else:
                print('No free player for sound')
        return playSound

try:
    app = QApplication([])
    w = MainWindow('/home/luvwahraan/NFS/Musique/SoundBank/')
    app.exec()
except KeyboardInterrupt:
    print('\nInterrupted by user')
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))


