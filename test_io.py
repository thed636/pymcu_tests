'''
Created on 21.11.2012

@author: deathbringer
'''

import pymcu           # Import the pymcu module


if __name__ == '__main__':
    mb = pymcu.mcuModule() # Initialize mb (My Board) with mcuModule Class Object - Find first available pymcu hardware module.
    mb.digitalState(1, 'input')
    count=0
    state=mb.digitalRead(1)
    while True :
        newState = mb.digitalRead(1)
        if state!=newState :
            count=count+1
            print 'count=%i' % count
            state=newState
