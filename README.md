# ws-zmq
Example project whith asynchronius web interface, web- and zmq- sockets.

Illustate using SUB\PUB and PUSH\PULL zmq patterns, aiohttp websockets and python async features.

Parts of project are:
 1. websockets.html - web interface 
 2. web_ws.py       - web server
 3. back-srv.py     - backend server

Brief description

 1. Initially events are generated by user's action. 
 2. Browser sends them to web-server via websocket. 
 3. Web-server pushes events to backend using ZeroMQ library. 
 4. Backend server process events and publishes result for web-server.
 5. Web-server sends result to all users via websockets.
 
Single backend serves many web-servers, single web-server serves many web-clients.
  
Requires pyhton3.7 or higher.

