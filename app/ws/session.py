from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter(prefix="/ws")


@router.websocket("/session")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    start = datetime.now()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
        except WebSocketDisconnect as e:
            print(f"connection duration {datetime.now()-start}")
            return
        