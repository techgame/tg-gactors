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

import gevent.event
from .ioActorDispatch import IOActorDispatch

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ IOActorObject -- this is not a required interface
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Future(gevent.event.AsyncResult): 
    pass

class IOActorObject(object):
    FutureResult = Future
    _amq_ = IOActorDispatch.property()

    def futureSend(self, fn, *args, **kw):
        fn = self._asSendMessageFn(fn)
        return self._amq_.sendMsg((fn, args, kw), self.FutureResult())

    def asyncSend(self, fn, *args, **kw):
        fn = self._asSendMessageFn(fn)
        return self._amq_.sendMsg((fn, args, kw), None)

    def _asSendMessageFn(self, fn):
        if isinstance(fn, basestring):
            fn = getattr(self, fn)
        try:
            if fn.im_self is self:
                return fn # allow instance methods
            elif fn.im_class is self.__class__:
                return fn # allow class methods
        except AttributeError: 
            pass

        raise ValueError("Expected bound method of "+self.__class__.__name__)

