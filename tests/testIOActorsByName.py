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

import math
import gactors
from gactors.ioActors import IOActorObject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ATestActor(IOActorObject):
    v = 0
    def getValue(self):
        return self.v
    def setValue(self, v):
        self.v = v

    def inc(self, x=1):
        self.v += x
        return self.v
    def log(self, x):
        return math.log(x, self.v)


def testIOActorsStandardObject():
    nk = ATestActor()
    assert nk.getValue() == 0
    nk.setValue(7)
    assert nk.getValue() == 7
    gactors.sleep(0)
    assert nk.getValue() == 7

def testIOActorsSimpleAsync():
    nk = ATestActor()
    nk.asyncSend('setValue', 24)
    assert nk.getValue() == 0
    gactors.sleep(0)
    assert nk.getValue() == 24
    nk.asyncSend('setValue', 7)
    assert nk.getValue() == 24
    gactors.sleep(0)
    assert nk.getValue() == 7
    gactors.sleep(0)
    assert nk.getValue() == 7

def testIOActorsFuture():
    nk = ATestActor()
    assert nk.getValue() == 0

    fv = nk.futureSend('inc')
    assert nk.getValue() == 0
    assert not fv.ready()

    r = fv.get()
    assert fv.ready()
    assert r == 1, r

def testIOActorsFutureException():
    nk = ATestActor()
    assert nk.getValue() == 0

    fv = nk.futureSend('log', 0)
    assert nk.getValue() == 0
    assert not fv.ready()

    try:
        r = fv.get()
        raise AssertionError("Should have raised a ValueError for log(0,0)")
    except ValueError, e:
        assert str(e) == "math domain error", e

    assert fv.ready()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    testIOActors()

