"""Example using zmq with asyncio coroutines"""
# Copyright (c) PyZMQ Developers.
# This example is in the public domain (CC-0)

import time

import zmq
from zmq.asyncio import Context, Poller
import asyncio

pull_url = 'tcp://127.0.0.1:3552'
pub_url = 'tcp://127.0.0.1:5554'

ctx = Context.instance()



async def transmitte():
    """receive messages with polling"""
    pull = ctx.socket(zmq.PULL)
    pull.connect(pull_url)
    poller = Poller()
    poller.register(pull, zmq.POLLIN)

    pub = ctx.socket(zmq.PUB)
    pub.bind(pub_url)

    while True:
        events = await poller.poll()
        if pull in dict(events):
            print("recving", events)
            msg = await pull.recv_multipart()
            print('recvd', msg)
            print(type(msg))
            await pub.send_multipart([b'new.event']+ msg)
            print('transmitted')





asyncio.get_event_loop().run_until_complete(asyncio.wait([
    transmitte(),
]))
