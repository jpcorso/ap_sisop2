import asyncio
import websockets

from asyncio import run
from asyncio import Future

from websockets import serve

sessions = {}
async def http_handler(path, headers):
    """Route HTTP requests to their handlers"""
    from http import HTTPStatus
    from websockets.http import Headers

    if path == '/ui-chat':
        # Entregar para o navegador o conteúdo do arquivo chat.html,
        # que corresponde ao cliente chat implementado pelo webservice
        with open("chat.html") as f:
            headers = Headers(**{'Content-Type': 'text/html'})
            body = bytes(f.read(), 'utf-8')

            return HTTPStatus.OK, headers, body

    elif path == '/ui-echo':
        # Entregar para o navegador o conteúdo do arquivo echo.html,
        # que corresponde ao cliente echo implementado pelo webservice
        with open("echo.html") as f:
            headers = Headers(**{'Content-Type': 'text/html'})
            body = bytes(f.read(), 'utf-8')

            return HTTPStatus.OK, headers, body
        
    else:
        return None

async def echo(websocket, sessions={}):
    
    """Chat WebSocket handler"""
    try:
        async for message in websocket:
            for socket in sessions.values():
                print(f"Sending message to {socket.remote_address}")
                await socket.send(message) 
    finally:
        print(f"Closing socket: {websocket.remote_address}")
        sessions.pop(websocket.remote_address)  

async def chat(websocket):
    
    """Chat WebSocket handler"""
    try:
        async for message in websocket:
            for socket in sessions.values():
                print(f"Sending message to {socket.remote_address}")
                await socket.send(message) 
    finally:
        print(f"Client Disconnected: {websocket.remote_address}")
        sessions.pop(websocket.remote_address)  

async def web_socket_router(websocket, path):
    remote = websocket.remote_address
    sessions[remote] = websocket
    print(f"Client connected: path={path}")
    """Route WebSocket requests to their handlers"""
    if path == '/':
        await websocket.close(reason=f'needs a path')
    elif path == '/echo':
        await echo(websocket)
    elif path == '/chat':
        await chat(websocket)
    else:
        await websocket.close(reason=f'path not found: {path}')


async def main():
    async with serve(web_socket_router, "localhost", 8080, process_request=http_handler):
        await Future()


run(main())
