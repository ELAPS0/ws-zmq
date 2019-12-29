#!/usr/bin/env python3
"""Example for aiohttp.web websocket server
"""

import os
import traceback

from aiohttp import web

import logging
import zmq
from zmq.asyncio import Context

WS_FILE = os.path.join(os.path.dirname(__file__), 'websocket.html')

sub_endpoint = 'tcp://127.0.0.1:5554'
push_endpoint = 'tcp://127.0.0.1:5552'

ctx = Context.instance()

class BusConnector:
    def __init__(self, topics = b''):
        '''
        ZMQ publish and subscribe sockets & utils
        @topics     - binary string representation (utf-8) list of subscription topics
        '''
        try:
            self.sub = ctx.socket(zmq.SUB)
            self.push = ctx.socket(zmq.PUSH)
            self.sub.setsockopt(zmq.SUBSCRIBE,topics.encode('utf-8'))
            self.sub.connect(sub_endpoint)
            self.push.bind(push_endpoint)
    
        except Exception as e:
            print("Error with sub world")
            print(e)
            logging.error(traceback.format_exc())
            print (traceback.format_exc())
            print()

    def add_topic(self, topic):
        self.sub.setsockopt(zmq.SUBSCRIBE,topic.encode('utf-8'))

    async def send_event(self, sender_id: str, msg:str):
        '''
        send event to zmq bus
        @sender_id  - websocket identity 
        @msg        - json message  type str
        '''
        print ('message {} is sending...'.format(msg))
        await self.push.send_multipart([sender_id.encode('utf-8'), msg.encode('utf-8')])

    async def get_events(self, app ):
        '''
        subscribe to zmq and get events
        @app      - main web application
        '''
        try:
            print("Receiving messages from {}...".format(sub_endpoint))
            while True:
                [topic, msg] = await self.sub.recv_multipart()
                print('   Topic: %s, msg:%s' % (topic, msg))
                for ws in app['sockets']:
                    if topic == b'broadcast' or topic == str(id(ws)).encode('utf-8'):
                        await ws.send_str(str(msg))

        except Exception as e:
            print("Error with sub world")
            print(e)
            logging.error(traceback.format_exc())
            print (traceback.format_exc())
            print()
        finally:
            print('Cancel zmq subscription...')
            #s.close()
            print('zmq connection closed.')



async def wshandler(request):
    resp = web.WebSocketResponse()
    available = resp.can_prepare(request)
    if not available:
        with open(WS_FILE, 'rb') as fp:
            return web.Response(body=fp.read(), content_type='text/html')
    
    request.app['bus'].add_topic(str(id(resp)))
    await request.app['bus'].send_event(str(id(resp)), 'init me')

    await resp.prepare(request)
    await resp.send_str('Welcome!!!')

    try:
        print('Someone joined.')
        for ws in request.app['sockets']:
            await ws.send_str('Someone joined')
        request.app['sockets'].append(resp)

        async for msg in resp:
            if msg.type == web.WSMsgType.TEXT:
                '''rems by bob
                for ws in request.app['sockets']:
                    if ws is not resp:
                        await ws.send_str(msg.data)
                '''
                await request.app['bus'].send_event('', msg.data)
            else:
                return resp
        return resp

    finally:
        request.app['sockets'].remove(resp)
        print('Someone disconnected.')
        for ws in request.app['sockets']:
            await ws.send_str('Someone disconnected.')



async def start_background_tasks(app):
    app['zmq_subscription'] = app.loop.create_task(app['bus'].get_events(app))

async def cleanup_background_tasks(app):
    print('cleanup background tasks...')
    app['zmq_subscription'].cancel()
    await app['zmq_subscription']


async def on_shutdown(app):
    for ws in app['sockets']:
        await ws.close()


def init():
    app = web.Application()
    app['sockets'] = []
    app['bus'] = BusConnector('broadcast')
    app.router.add_get('/', wshandler)
    #app.router.add_get([web.static('/static', 'static')])
    app.add_routes    ([web.static('/static', 'static')])
   

    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    app.on_shutdown.append(on_shutdown)
    return app

web.run_app(init())

