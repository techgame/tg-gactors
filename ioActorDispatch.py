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

import sys
import gevent
from .actorFactory import ActorFactory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ IO Actor Dispatch -- to keep the actors simple
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IOActorDispatch(object):
    factory = ActorFactory()
    def __init__(self, fnDispatch=None):
        if fnDispatch is None:
            fnDispatch = self._fnDispatchDefault
        self.rawSendMsg = self._spawnActor(self._dispatchLoop, fnDispatch)

    def sendMsg(self, msg, future=None):
        self.rawSendMsg((msg, future))
        return future
    __call__ = sendMsg

    def exit(self, block=True, timeout=None):
        if self._gltLoop is not None:
            self._gltLoop.kill(block=block, timeout=timeout)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Dispatch Loop 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def _fnDispatchDefault(msg):
        fn, args, kw = msg
        return fn(*args, **kw)

    _gltLoop = None
    def _dispatchLoop(self, recvMsg, fnDispatch):
        self._gltLoop = gevent.getcurrent()
        try:
            while 1:
                r = None # clear out message
                msg, future = recvMsg()
                try:
                    r = fnDispatch(msg)
                except Exception, e:
                    self._dispatchException(future, e)
                else:
                    if future is not None:
                        future.set(r)

        except gevent.GreenletExit:
            self._gltLoop = None

    def _dispatchException(self, future, e):
        sys.excepthook(*sys.exc_info())
        if future is not None:
            future.set_exception(e)

    @classmethod
    def _spawnActor(klass, anActorFn, fnDispatch):
        """Override to use a different factory method"""
        return klass.factory.spawnActor(anActorFn, fnDispatch)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def property(klass, fnDispatch=None, attrName=None, desc=None):
        """A property for lazy creation of an ActorDispatch"""

        if attrName is None:
            attrName = '__an_'+klass.__name__

        def getIOActorDispatch(inst):
            r = getattr(inst, attrName, None)
            if r is None:
                r = klass(fnDispatch)
                setattr(inst, attrName, r)
            return r
        def delIOActorDispatch(inst):
            r = getattr(inst, attrName, None)
            if r is not None:
                r.exit()
                delattr(inst, attrName)

        return property(getIOActorDispatch, None, delIOActorDispatch, desc)

