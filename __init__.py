##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2010  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

"""Channel based actor implementation for gevent library.

>>> import gactors
>>> def anActor(recvMsg): 
...     while 1: print 'actor received: '+ recvMsg()
>>> sendMsg = gactors.spawn(anActor)
>>> sendMsg("hello actor!")
>>> gactors.sleep(0)
actor received: hello actor!
>>> sendMsg("goodnight actor")
>>> gactors.sleep(0)
actor received: goodnight actor
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from gevent import sleep
from .actorFactory import ActorFactory, PriorityActorFactory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Factory instance and spawnActor method
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_factory = ActorFactory()
spawnActor = _factory.spawnActor
spawn = spawnActor

