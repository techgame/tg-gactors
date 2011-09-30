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

import gevent
import gevent.queue

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def bindChannelRaw(mq=None):
    """A simple message channel connected by a queue. Returns (sendMsg, recvMsg)"""
    if mq is None:
        mq = gevent.queue.Queue()
    def sendMsg(msg):
        mq.put(msg)
    def recvMsg(block=True, timeout=None):
        return mq.get(block, timeout)
    return sendMsg, recvMsg
bindChannel = bindChannelRaw

def spawnActorRaw(anActorFn, *args, **kw):
    """A simple actor spawning method using channels.  
    The actor is spawned using anActorFn with recvMsg as the first parameter,
    and this function returns sendMsg"""
    sendMsg, recvMsg = bindChannelRaw()
    gevent.spawn_link_exception(anActorFn, recvMsg, *args, **kw)
    return sendMsg
spawnActor = spawnActorRaw

