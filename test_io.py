'''
Created on 21.11.2012

@author: deathbringer
'''

import pymcu           # Import the pymcu module
import time

class InputTtlPin :
    def __init__(self,board,pin):
        self.board = board
        self.pin = pin
        self.board.digitalState(self.pin,'input')
        self.state = self.read()
        self.triggerCount = 0
    
    def read(self):
        return self.board.digitalRead(self.pin)
    
    def trigger(self):
        newState = self.read()
        if self.state != newState :
            self.triggerCount = self.triggerCount+1
            self.state = newState
            #print 'newState=%s, state=%s, count=%s' %(newState, self.state,self.triggerCount)
            return True
        return False
    
    def resetTriggerCount(self):
        self.triggerCount = 0
    
    def triggerPulseCount(self):
        self.triggerCount = self.triggerCount+self.board.pulseCount(self.pin, 10)
        return self.triggerCount

def checkReadSpeed(mb):
    t = time.time()
    mb.digitalState(1,'input')
    for i in range(1,1000) :
        mb.digitalRead(1)
    print time.time() - t

def stop(mb):
    mb.digitalState(11, 'output')
    mb.digitalState(12, 'output')
    mb.pinLow([11,12])
    mb.pwmOff(1)

def rotate(mb):
    mb.digitalState(11, 'output')
    mb.digitalState(12, 'output')
    mb.pinLow([11,12])
    mb.pwmOff(1)
    mb.pwmDuty(1, 880)
    mb.pinHigh(12)
    mb.pwmOn(1)
    pin = InputTtlPin(mb,1)
    while pin.triggerPulseCount() <20 :
        pass
        #pin.trigger()
        #mb.pausems(1)
#    mb.pwmOff(1)
#    mb.pwmDuty(1, 0)
#    pin.resetTriggerCount()
#    mb.pinToggle([11,12])
#    while pin.triggerCount !=20 :
#        pin.trigger()
        #mb.pausems(1)
    mb.pinLow([11,12])
    mb.pwmOff(1)
    print pin.triggerCount

def countImpulse(mb):
    mb.digitalState(1, 'input')
    count=0
    state=mb.digitalRead(1)
    while True :
        newState = mb.digitalRead(1)
        if state!=newState :
            count=count+1
            print 'count=%i' % count
            state=newState

if __name__ == '__main__':
    mb = pymcu.mcuModule() # Initialize mb (My Board) with mcuModule Class Object - Find first available pymcu hardware module.
    checkReadSpeed(mb)
    stop(mb)
    try:
        rotate(mb)
    finally:
        stop(mb)
