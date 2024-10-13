import jack
import queue
import soundfile as sf
import numpy as np
from PyQt5.QtCore import QRunnable, QObject, QThreadPool
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
import threading

class Signals(QObject):
    started = Signal(int, str)
    completed = Signal(int, str)

class JackPlayer(QRunnable):
    def __init__(self, n, sf_path, clientname='JackSoundinB', buffersize=16):
        super().__init__()
        self.n = n
        self.soundfilename = sf_path
        self.clientname = f"{clientname}_{self.n}"
        self.buffersize = buffersize
        self.signals = Signals()
        self.event = threading.Event()

        self.q = queue.Queue(maxsize=self.buffersize)

        # jack client
        self.client = jack.Client(self.clientname)
        self.blocksize = self.client.blocksize
        self.samplerate = self.client.samplerate
        self.client.set_xrun_callback(self.xrun)
        self.client.set_shutdown_callback(self.shutdown)
        self.client.set_process_callback(self.process)

    @Slot()
    def run(self):
        self.signals.started.emit(self.n, self.soundfilename)
        
        try:
            with sf.SoundFile(self.soundfilename) as f:
                # register ports
                for ch in range(f.channels):
                    self.client.outports.register(f'out_{ch + 1}')
                
                # fill queue for audio data
                block_generator = f.blocks( blocksize=self.blocksize, \
                        dtype='float32', always_2d=True, fill_value=0 )
                
                for _, data in zip(range(self.buffersize), block_generator):
                    self.q.put_nowait(data)
                
                with self.client:
                    timeout = self.blocksize * self.buffersize / self.samplerate
                    for data in block_generator:
                        self.q.put(data, timeout=timeout)
                    
                    self.q.put(None, timeout=timeout)
                    self.event.wait()
                
            self.signals.completed.emit(self.n, self.soundfilename)

        except Exception as e:
            print(f"Error: {e}")

    def process(self, frames):
        if frames != self.blocksize:
            self.stop_callback('blocksize problem')
        
        try:
            data = self.q.get_nowait()
        except queue.Empty:
            self.stop_callback('Empty buffer, increase buffersize.')

        # stop when playback finished
        if data is None:
            self.stop_callback()
        else:
            try:
                # audio data to jack ports
                for channel, port in zip(data.T, self.client.outports):
                    port.get_array()[:] = channel
            except Exception as e:
                print( type(e).__name__ + ': ' + str(e) )


    def xrun(self, delay):
        print(f"Xrun, delay : {delay}.")

    def shutdown(self, status, reason):
        print(f"JACK shudown, statut : {status}, raison : {reason}.")
        self.event.set()

    def stop_callback(self, msg=''):
        if msg:
            print(f"Error : {msg}")

        for port in self.client.outports:
            port.get_array().fill(0)
        self.event.set()
        
        raise jack.CallbackExit
        
