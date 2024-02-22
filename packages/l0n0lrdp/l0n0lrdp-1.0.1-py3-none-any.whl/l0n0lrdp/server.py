import os
import sys
import aiohttp
import argparse
from aiohttp import web
from typing import Dict

max_id = 0
clients: Dict[str, web.WebSocketResponse] = {}
async def broad_cast_json(msg):
    for client in clients.values():
        await client.send_json(msg)

async def handler(request:web.Request):
    client = web.WebSocketResponse()
    await client.prepare(request)
    global max_id
    id = max_id
    max_id += 1
    clients[id] = client
    await client.send_json({"type": "id", "id": id})
    await broad_cast_json({"type": "id_list", "ids": list(clients.keys())})
    async for msg in client:
        if msg.type == aiohttp.WSMsgType.TEXT:
            json_msg = msg.json()
            target_client = clients.get(json_msg['target_id'])
            if target_client is not None:
                await target_client.send_str(msg.data)
            else:
                await broad_cast_json(json_msg)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            break
    del clients[id]
    await broad_cast_json({"type": "id_list", "ids": list(clients.keys())})
    print(id, "closed")

def start_server():
    parser = argparse.ArgumentParser(description="录屏观看")
    # 定义 listen 选项
    parser.add_argument(
        "-l",
        "--listen",
        metavar="HOST:PORT",
        default="0.0.0.0:5500",
        help="要监听的IP:端口",
    )
    # 解析参数
    args = parser.parse_args()
    listen_host, listen_port = args.listen.split(":")
    app = web.Application()
    file_dir = sys.argv[0]
    server_dir, _ = os.path.split(file_dir)
    if not os.path.exists(f'{server_dir}/index.html'):
        server_dir, _ = os.path.split(__file__)
        if not os.path.exists(f'{server_dir}/index.html'):
            print(server_dir)
            print("启动错误，没有找到index.html")
            return
    app.add_routes([
        web.get("/ws", handler),
        web.static("/", server_dir),
    ])
    web.run_app(app, host=listen_host, port=int(listen_port))

if __name__ == "__main__":
    start_server()
    

