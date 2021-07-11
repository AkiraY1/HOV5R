from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from trackingModule import handDetector

class volumeControl():
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    def getVolume(self):
        currentVolumeDb = self.volume.GetMasterVolumeLevel()
        return currentVolumeDb

    def getRange(self):
        volumeRange = self.volume.GetVolumeRange()
        return volumeRange

    def setVolume(self, vr):
        self.volume.SetMasterVolumeLevel(vr, None)