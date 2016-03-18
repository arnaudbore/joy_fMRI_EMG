#from __future__ import division
import labjack_interface as lji

# PARAMETERS
param = {'nbKeys':12,
         'seqUsed':[1,2,3,1,4,2,4,3,2,1,3,4],
         'nbBlocs':2}

IO1_M = {'nb_rep':1,
       'channel':3,
       'width_w_impulse':0.001,
       'width_wo_impulse':0.100,
       }

IO2_R = {'nb_rep':50,
       'channel':5,
       'width_w_impulse':0.001,
       'width_wo_impulse':0.5,
       }

#ISI = 0.5
#TR = 0.1

#PATH = '/home/borear/workspace/joystick/src/'
#SUBJECT_ID = 'subject_id.txt'

#f = open(PATH+SUBJECT_ID, 'w')
#f.write(SUBJECT_ID+' \n')

lji.start_labjack()


#end_stimulation = lji.run_stimulation(f,IO2_R)
#end_stimulation = lji.run_stimulation(f,IO1,IO2,ISI,TR)




