##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2010  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

"""Channel based actor implementation for gevent library"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import gevent
import gevent.queue
import gevent.pool

from .utils import assignBoundNames

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SimpleActorFactory(object):
    """A simple actor factory without the override points of ActorFactory"""

    def spawnActor(self, anActorFn, *args, **kw):
        """Spawns a new greenlet actor and returns a method to send messages to the actor.
        Args and keywords are passed to anActorFn after bound recvMsg function."""
        gevent.spawn_link_exception(anActorFn, recvMsg, *args, **kw)
        return sendMsg

    def bindChannel(self, mq=None):
        """Returns (sendMsg, recvMsg) functions connected to the same message queue"""
        if mq is None:
            mq = gevent.queue.Queue()
        def sendMsg(msg):
            mq.put(msg)
        def recvMsg(block=True, timeout=None):
            return mq.get(block, timeout)
        return sendMsg, recvMsg

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ActorFactory(object):
    """An extensible actor spawning factory.
    
    Override to provide factories for MsgQueue or ActorGroup, or
    reimplement any of the bind* methods to provide custom semantics.
    """
    MsgQueue = gevent.queue.Queue
    ActorGroup = gevent.pool.Group
    
    def spawnActor(self, anActorFn, *args, **kw):
        """Spawns a new greenlet actor and returns a method to send messages to the actor.
        Args and keywords are passed to anActorFn after bound recvMsg function."""
        
        spawnActor = self.bindAsActor(anActorFn)
        return spawnActor(*args, **kw)
    __call__ = spawnActor

    def iterSpawnActor(self, anActorFn, *args, **kw):
        """Iteralbe version of spawnActor with each actor being connected to the same channel"""
        spawnActor = self.bindAsActor(anActorFn)
        while 1:
            yield spawnActor(*args, **kw)

    def bindAsActor(self, anActorFn):
        """Returns a bound method for spawning a new actor, returning sendMsg method"""
        sendMsg, recvMsg = self.bindChannel()
        spawn = self.bindSpawn(anActorFn, sendMsg, recvMsg)
        assignBoundNames(anActorFn, [sendMsg, recvMsg, spawn])
        return spawn

    def bindChannel(self, mq=None):
        """Returns (sendMsg, recvMsg) functions connected to the same message queue"""
        if mq is None:
            mq = self.MsgQueue()

        def sendMsg(msg):
            mq.put(msg, False)
        def recvMsg(block=True, timeout=None):
            return mq.get(block, timeout)
        return sendMsg, recvMsg

    def bindSpawn(self, anActorFn, sendMsg, recvMsg):
        """Override to bind a different actors spawn implementation"""
        actors = self.ActorGroup()
        sendMsg.actors = recvMsg.actors = actors
        def spawn(*args, **kw):
            actors.spawn_link_exception(anActorFn, recvMsg, *args, **kw)
            return sendMsg
        return spawn

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PriorityActorFactory(ActorFactory):
    Queue = gevent.queue.PriorityQueue

