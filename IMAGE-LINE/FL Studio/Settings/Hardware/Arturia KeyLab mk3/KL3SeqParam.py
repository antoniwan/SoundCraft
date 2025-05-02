import channels
import patterns
import KL3Process as PR

# This script contains fonctions that modify Bit parameter in Step Sequencer
     
PARAM_TYPE_LIST = {
    '91':0,
    '92':1,
    '94':2,
    '95':3,
    '96':4,
    '97':5,
    '102':6,
    '103':7,
}


def Param(event) :

    channel = channels.selectedChannel()
    pattern = patterns.patternNumber()
    delta = (event.data2 - 64)
    center = min(PR.INDEX_PRESSED)+(8*PR.SEQUENCER_PAGE)
        
    PARAM_TYPE = PARAM_TYPE_LIST.get(str(event.controlNum))

    for i in PR.INDEX_PRESSED :
        if PARAM_TYPE != 7 :
            step = i+(8*PR.SEQUENCER_PAGE)
            value = channels.getCurrentStepParam(channel, step, PARAM_TYPE)
            channels.setStepParameterByIndex(channel, pattern, step, PARAM_TYPE, value + delta, 0)
    
            channels.showGraphEditor(0,PARAM_TYPE,center,channel,0)



    # UTILITY
