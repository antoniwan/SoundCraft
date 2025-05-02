from KLEss3Dispatch import send_to_device

from MachineState import eMachineState

# This class handles the connexion messages


class KLEssConnexion :
    
    def __init__(self):
        
        self._isArturia = 0
        self._isDAW = 0
        
        
    def ArturiaConnexion(self) :
        #print("Arturia Connecté")
        send_to_device(bytes([0x02, 0x0F, 0x40, eMachineState.eArturiaConnected, 0x01]))
        self._isArturia = 1
        
    def ArturiaDisconnection(self) :
        #print("Arturia Deconnecté")
        send_to_device(bytes([0x02, 0x0F, 0x40, eMachineState.eArturiaConnected, 0x00]))
        self._isArturia = 0
        
    def DAWConnexion(self) : 
        #print("DAW Connecté")
        send_to_device(bytes([0x02, 0x0F, 0x40, eMachineState.eDawConnected, 0x01]))
        self._isDAW = 1
        
    def DAWDisconnection(self) : 
        #print("DAW déconnecté")
        send_to_device(bytes([0x02, 0x0F, 0x40, eMachineState.eDawConnected, 0x00]))
        self._isDAW = 0
        
    def MemoryRequest(self) :
        #print("Requête mémoire")
        send_to_device(bytes([0x01, 0x11, 0x40, 0x5c]))

        