from PyQt5.QtCore import QRunnable, QObject, QThreadPool
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

import os

class Signals(QObject):
    started = Signal(int)
    completed = Signal(int)

"""
Get a soundfile and plays it throut jackd

TODO
Remove implement a jack player to remove jack-play
"""
class JackPlayer(QRunnable):
    def __init__(self, n, sf):
        super().__init__()
        self.n = n
        self.soundfile = sf
        self.signals = Signals()
        
    @Slot()
    def run(self):
        self.signals.started.emit(self.n)
        os.system(f"jack-play -un JackSoundinB_{self.n} '{self.soundfile}'")
        self.signals.completed.emit(self.n)
