from PyQt5.QtCore import QRunnable, QObject, QThreadPool
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
import queue

import os

class Signals(QObject):
    started = Signal(int, str)
    completed = Signal(int, str)

"""
Get a soundfile and plays it throut jackd

TODO
Remove implement a jack player to remove jack-play
"""
class JackPlayer(QRunnable):
    def __init__(self, n, sf=False, max_queue=3):
        super().__init__()
        self.n = n
        self.signals = Signals()
        
        self.running = True
        
        self.soundQueue = queue.Queue( max_queue )
        if sf:
            self.queueSound(sf)
    
    def terminate(self):
        self.running = False
        
        # Add empty soundfile in queue to force self.run update
        self.queueSound('')
    
    def queueSound(self, sf):
        try:
            self.soundQueue.put_nowait( sf )
            return True
        except queue.Full:
            return False
        except Exception as e:
            print('JackPlayer addQueue ' + type(e).__name__ + ': ' + str(e))
        
    @Slot()
    def run(self):
        print(f"Running thread player {self.n}")
        while self.running:
            try:
                # wait for soundfile in queue
                sf = self.soundQueue.get()                
                
                self.signals.started.emit(self.n, sf)
                os.system(f"jack-play -un JackSoundinB_{self.n} '{sf}' 1> /dev/null")
                self.signals.completed.emit(self.n, sf)
            except queue.Empty:
                continue
            except Exception as e:
                print('JackPlayer runner' + type(e).__name__ + ': ' + str(e))
        
