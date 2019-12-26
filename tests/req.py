import traceback
import zmq
import asyncio
from zmq.asyncio import Context

req_url     = 'tcp://127.0.0.1:5555'



async def request(r):
    try:
        print ('start ', r.decode('utf-8'))
        req = Context.instance().socket(zmq.REQ)
        req.connect(req_url)
        await req.send(r)
        msg = await req.recv()
        print ('got answer: {}'.format(msg.decode('utf-8')))
    except Exception as e:
        print("Error with sub world")
        print(e)
        print (traceback.format_exc())
        print()

async def do_req():
    try:
        for i in range(2):
            r = 'init me {}'.format(i).encode('utf-8')
            asyncio.ensure_future(request(r))
    except Exception as e:
        print(e)
        print (traceback.format_exc())
        print()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_req())


