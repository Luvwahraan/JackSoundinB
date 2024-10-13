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
from PyQt5.QtWidgets import QToolBar, QPushButton, QToolButton


from JackPlayer import *
from DirsTabWidget import *

        

#class Window(QWidget):
class MainWindow(QMainWindow):
    
    def clearAndQuit(self):
        # Force all threads to terminate tasks
        for player in range(0, self.maxPlayers):
            self.players[player].terminate()
        
        print(f"Played {self.stats['played']} sounds.")
        
        self.close # Doesn't work??
        
    
    def __init__(self, sound_directory, max_players=2, max_queue=2):
        super(MainWindow, self).__init__()
        self.setWindowTitle("JackSoundinB")
        
        self.maxPlayers = max_players
        self.maxQueue = max_queue
        
        self.width = 800
        self.setGeometry(2520, 1080, self.width, 500)
        
        self.iconSize = 50
        
        self.soundDirectory = sound_directory
        self.imgDirectory = os.path.join(self.soundDirectory, 'icons')
        
        # Jackd players, in threads.
        self.pool = QThreadPool.globalInstance()
        self.players = []
        self.currentPlayer = 0
        
        self.stats = {}
        self.stats['played'] = 0
        
        # Create started threads, waiting for soundfile to be queued
        for player in range(0, self.maxPlayers):
            print(f"Creating player {player}")
            
            self.players.append(JackPlayer(player, False, self.maxQueue) )
            
            self.players[player].signals.started.connect( self.startedSound )
            self.players[player].signals.completed.connect( self.finishedSound )
            
            self.pool.start( self.players[player] )
        
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
        #print(f"Creating layout {layout}")
        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)
        
        maxCol = int( self.width / ( self.iconSize + 15 ) )
        row = 0
        column = 0

        for sf in filenames:
            filename,ext = os.path.splitext( sf )
            soundfile = os.path.join(current_path, sf)
            button = QToolButton()
            
            # Use clear icon if no one found
            img = os.path.join( self.imgDirectory, f"{filename}.png" )
            if not os.path.exists(img):
                img = os.path.join( self.imgDirectory, 'clear.png' )
                
            button.setIcon( QtGui.QIcon(img) )
            button.setIconSize( QtCore.QSize(self.iconSize, self.iconSize) )
            button.clicked.connect( self.playSoundSignal(soundfile) )
            button.setToolTip( filename )
            
            grid.addWidget(button, row, column)

            # Adapt grid to window width
            column += 1
            if column >= maxCol:
                column = 0
                row += 1
        
        # Quit button on each directory
        quitButton = QPushButton('Quit')
        quitButton.clicked.connect( self.clearAndQuit )
        grid.addWidget(quitButton)
            
        self.tabWidget.addNewTab( grid, layout, self.imgDirectory )


    """
    Threads handles
    """
    def startedSound(self, n, sf=''):
        #self.players.append(n)        
        filename = os.path.splitext( list(os.path.split( sf ))[1] )[0]
        self.tabWidget.fillChannel(n, filename)
        
    def finishedSound(self, n, sf=''):
        #self.players.remove(n)
        self.tabWidget.freeChannel(n)
    
    def playSoundSignal(self, soundfile):
        def playSound():
            try:
                # Try each player for free queue
                soundQueued = False
                for timeout in range(0, self.maxPlayers):
                    print(f"Trying to fill player {self.currentPlayer} {timeout}")
                    soundQueued = self.players[self.currentPlayer].queueSound(soundfile)
                    
                    print(soundQueued)
                    
                    # Change next player who get soundfile
                    self.currentPlayer += 1
                    if self.currentPlayer >= self.maxPlayers:
                        self.currentPlayer = 0
                    
                    if soundQueued:
                        self.stats['played'] += 1
                        break
                
            except Exception as e:
                print('playSoundSignal ' + type(e).__name__ + ': ' + str(e))                
        return playSound

try:
    app = QApplication([])
    w = MainWindow('/home/luvwahraan/NFS/Musique/SoundBank/')
    app.exec()
except KeyboardInterrupt:
    print('\nInterrupted by user')
except Exception as e:
    print('JackSoundinB ' + type(e).__name__ + ': ' + str(e))


