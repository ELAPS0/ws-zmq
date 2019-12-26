import sys
import traceback
import asyncio
from mdcliapi2 import MajorDomoClient
req_url     = 'tcp://127.0.0.1:5555'
verbose = '-v' in sys.argv
cli = MajorDomoClient(req_url, verbose)


async def get_rep(i):
    print ('future ', i)
    msg = cli.recv()
    print(msg)
    #print ('got answer: {}'.format(msg.decode('utf-8')))
async def do_req():
    try:
        for i in range(2):
            try:
                r = 'request {}'.format(i)
                print ('start ',r) 
                cli.send(b'ping', r.encode('utf-8'))
                asyncio.ensure_future(get_rep(i))
            except Exception as e:
                print("Error with sub world")
                print(e)
                print (traceback.format_exc())
                print()
    except Exception as e:
        print(e)
        print (traceback.format_exc())
        print()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_req())


