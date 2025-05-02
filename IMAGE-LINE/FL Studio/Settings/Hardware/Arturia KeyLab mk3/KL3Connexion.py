from KL3Dispatch import send_to_device

from IntegrationPatchId import eIntegrationPatchId
from ParamId import eParamId

# This class handles the connexion messages


class Connexion :
    
    def __init__(self):
        
        self._isArturia = 0
        self._isDAW = 0
        
        
    def ArturiaConnexion(self) :
        send_to_device(bytes([0x00, eIntegrationPatchId.eArturia, eParamId.eConnection, 0x01]))
        self._isArturia = 1
        
    def ArturiaDisconnection(self) :
        send_to_device(bytes([0x00, eIntegrationPatchId.eArturia, eParamId.eConnection, 0x00]))
        self._isArturia = 0
        
    def DAWConnexion(self) : 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eConnection, 0x01]))
        self._isDAW = 1
        
    def DAWDisconnection(self) : 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eConnection, 0x00]))
        self._isDAW = 0


        