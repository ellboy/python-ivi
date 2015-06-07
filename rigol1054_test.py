'''
Created on 23.05.2015

@author: drakon
'''

# import usbtmc
# instr =  usbtmc.Instrument(6833, 1230)
# print(instr.ask("*IDN?"))

import ivi
 
     
  
if __name__ == '__main__':
    #print(globals())
    #mso = ivi.agilent.agilentMSO7104A("TCPIP0::192.168.1.104::INSTR")
    #ivi1 = ivi.ivi()
    mso = ivi.rigol.rigolDS1054("USB0::6833::1230::INSTR", simulate=True)
    #mso = ivi.agilent.agilentMSO7104A("simulate")
    mso.display.clear()
#    mso.channels[0].label = 'g'
    mso.acquisition.time_per_record = 1e-3
#    mso.trigger.type = 'edge'
#     mso.trigger.source = 'channel1'
#     mso.trigger.coupling = 'dc'
#     mso.trigger.edge.slope = 'positive'
#     mso.trigger.level = 0
    mso.channels['channel1'].enabled = False
    mso.channels['channel2'].enabled = False
    mso.channels['channel1'].enabled = True
    mso.channels['channel2'].enabled = False
    
    mso.channels['channel1'].coupling = 'dc'
    
    #print(mso.channels['channel1'].coupling)
    mso.channels['channel1'].offset = 1
    print mso.channels['channel1'].offset
    
    #mso.channels['channel1'].range = 1
    print mso.channels[0].range
    #mso.channels['channel1'].coupling = 'dc'
    mso.measurement.initiate()
    waveform = mso.channels[0].measurement.fetch_waveform()
    vpp = mso.channels[0].measurement.fetch_waveform_measurement("voltage_peak_to_peak")
    print vpp
#     phase = mso.channels['channel1'].measurement.fetch_waveform_measurement("phase", "channel2")