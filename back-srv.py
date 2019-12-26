"""Example using zmq with asyncio coroutines"""
# Copyright (c) PyZMQ Developers.
# This example is in the public domain (CC-0)

import time

import zmq
from zmq.asyncio import Context, Poller
import asyncio

pull_url    = 'tcp://127.0.0.1:3552'
pub_url     = 'tcp://127.0.0.1:5554'
rep_url     = 'tcp://127.0.0.1:5555'

ctx = Context.instance()
def msg_proc(msg):
    '''
    message processor 
    @msg    - zmq message (list of binary string (utf-8))
    @return   - list [topic, response_message]
    '''
    return [b'new event', msg[0]+b' processed']

async def request_handler():
    '''
    client single request handler
    '''
    rep = ctx.socket(zmq.REP)
    rep.connect(rep_url)
    msg = await rep.recv()
    print ('got request {}'.format(msg))
    await rep.send('done') 

async def events_handler():
    '''
    client events handler
    receive from web server, icall processor and transmit result  back as event  
    '''

    pull = ctx.socket(zmq.PULL)
    pull.connect(pull_url)
    poller = Poller()
    poller.register(pull, zmq.POLLIN)

    pub = ctx.socket(zmq.PUB)
    pub.bind(pub_url)

    while True:
        events = await poller.poll()
        if pull in dict(events):
            msg = await pull.recv_multipart()
            await pub.send_multipart(msg_proc( msg))
            print('recvd {}, transmetted'.format(msg))

asyncio.get_event_loop().run_until_complete(asyncio.wait([
    events_handler(),
    request_handler()
]))

