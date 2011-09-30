#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2010  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import gactors

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@gactors.spawnActor
def actorA(recvMsg):
    while 1:
        v, lst = recvMsg()
        lst.append(('A', v))
        if v <= 0: break
        actorB((v-1, lst))

    actorB((None, lst))

@gactors.spawnActor
def actorB(recvMsg):
    while 1:
        v, lst = recvMsg()
        lst.append(('B', v))
        if v <= 0: break
        actorC((v-1, lst, actorA))

    actorC((None, lst, actorA))

@gactors.spawnActor
def actorC(recvMsg):
    while 1:
        v, lst, anActor = recvMsg()
        lst.append(('C', v))
        anActor((v, lst))
        if v <= 0: break

def testActorMsgPassing():
    lst = []
    allActors = [actorA, actorB, actorC]
    actorC((5, lst, actorA))

    while not all(g.ready() for a in allActors for g in a.actors):
        gactors.sleep(0)

    lstKnownGood = [
        ('C', 5), ('A', 5), ('B', 4),
        ('C', 3), ('A', 3), ('B', 2),
        ('C', 1), ('A', 1), ('B', 0),
        ('C', None), ('A', None),]

    assert lst == lstKnownGood

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    testActorMsgPassing()
