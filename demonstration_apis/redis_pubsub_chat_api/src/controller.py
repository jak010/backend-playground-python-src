import asyncio
import json

from fastapi import WebSocket, Depends, Path, WebSocketDisconnect, Body
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from src.utils import ConnectionManager, AsyncRedisClient

controller_router = APIRouter(tags=['API'], prefix="")
websocket_router = APIRouter(tags=['API'], prefix="")

redis_client = AsyncRedisClient()


@controller_router.get("/")
def hello_world():
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat</title>
        </head>
        <body>
            <h1>WebSocket Chat</h1>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>
                var ws_url = "ws://localhost:8000/ws"
                var client_id = crypto.randomUUID()
                
                var ws = new WebSocket(ws_url + "/" + client_id );
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                function sendMessage(event) {
                    var input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = ''
                    event.preventDefault()
                }
            </script>
        </body>
    </html>
    """

    return HTMLResponse(html)


@controller_router.get("/enter_room")
def enter_room_view():
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat</title>
        </head>
        <body>
            <h1>WebSocket Chat</h1>
            <form action="" onsubmit="enterRoome(event)">
                <input type="text" id="roomName" autocomplete="off"/>
                <button>EnterRoom</button>
            </form>
            
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            
            <ul id='messages'>
            </ul>
            <script>
            
                                            
                function enterRoome(event) {
                    event.preventDefault()
                    var input = document.getElementById("roomName")
                    var ws_url = "ws://localhost:8000/ws/room/" + input.value;                                                                                                                                                                        
                    var ws = new WebSocket(ws_url);
                    
                    ws.onmessage = function(event) {
                        var messages = document.getElementById('messages')
                        var message = document.createElement('li')
                        var content = document.createTextNode(event.data)
                        message.appendChild(content)
                        messages.appendChild(message)
                    };                                                            
                                        
                    ws.send(input.value)
                    input.value = ''                    
                }
                
                async function sendMessage(event) {
                    event.preventDefault();
                    
                    var room_name = document.getElementById("roomName");
                    var send_message = document.getElementById("messageText");

                    var api_url = "http://localhost:8000/room/" + room_name.value + "/message";
                    
                    try {
                        const response = await fetch(api_url, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/multipart-form',
                            },
                             body: JSON.stringify({ message: send_message.value }), 
                        });
                
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                
                        // Optional: Handle the response if needed
                        const data = await response.json();
                
                        // Clear the input field after successful submission
                        send_message.value = '';
                
                    } catch (error) {
                        console.error('Error during fetch operation:', error);
                    }
                }

                                                                
            </script>
        </body>
    </html>
    """

    return HTMLResponse(html)


@websocket_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str = Path(), manager: ConnectionManager = Depends(ConnectionManager)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(message=data, websocket=websocket)
            await manager.broadcast(f"Client_id: {client_id}")
    except  WebSocketDisconnect:
        manager.disconnect(websocket)


@websocket_router.websocket("/ws/room/{room_name}")
async def websocket_endpoint_v1(websocket: WebSocket, room_name: str = Path(), manager: ConnectionManager = Depends(ConnectionManager)):
    await manager.connect(websocket)

    pubsub = redis_client.client.pubsub()
    await pubsub.subscribe(room_name)

    try:
        while True:
            await asyncio.sleep(0.01)  # asyncio.exceptions.CancelledError
            message = await pubsub.get_message()
            if message is not None:
                await  websocket.send_text(str(message['data']))

    except WebSocketDisconnect as e:
        await manager.disconnect(websocket)


@websocket_router.post("/room/{room_name}/message")
async def websocket_endpoint_v1(
        room_name: str = Path(),
        data=Body(default=None)

):
    receive_data = json.loads(data)

    await asyncio.sleep(0.01)
    await redis_client.client.handle_event(channel=room_name, message=str(receive_data['message']))
