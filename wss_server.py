import asyncio
import websockets
import os
import sys
import importlib
import glob
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def errlog(a):
    sys.stderr.write(a+"\n")

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filepath, notify_func, loop):
        self.filepath = filepath
        self.notify_func = notify_func
        self.loop = loop

    def on_modified(self, event):
        if event.src_path == self.filepath:
            asyncio.run_coroutine_threadsafe(self.notify_func(), self.loop)

def call_function(function_name, function_data):
    files = glob.glob("./func*_*.py")[::-1]
    
    for file in files:
        base_name = os.path.basename(file)
        module_name = base_name.split('.')[0]

        # Import the module
        module = importlib.import_module(module_name)
        # Reload to get the latest version
        module = importlib.reload(module)

        # Check if the module has the desired function
        function_scv_name = "func_"+function_name
        if not hasattr(module, function_scv_name): continue

        try:
            function = getattr(module, function_scv_name)
            response = function(function_data)
            return response
        except AttributeError as e:
            errlog(f"[{base_name}]Caught an attribute error: {e}")
            pass
    # If the function is not found in any of the modules, return None
    return {"data":f"[{function_name}] not defined", "status":"fail"}

async def notify_clients():
    if clients:
        try:
            data = {'func': 'status'}
            func = data.get('func', '')
            response = call_function(func, data)
            response = json.dumps(response)
            for client in clients:
                await client.send(response)
        except Exception as e:
            print(f"Failed to read or send file content: {e}")

async def main():
    global clients
    clients = set()
    loop = asyncio.get_running_loop()
    observer = Observer()
    event_handler = FileChangeHandler('/dev/shm/station/WSOCKET', notify_clients, loop)
    observer.schedule(event_handler, path='/dev/shm/station', recursive=False)
    observer.start()

    async with websockets.serve(handler, "0.0.0.0", 5000):
        await asyncio.Future()  # Run forever

async def handler(websocket, path):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

if __name__ == "__main__":
    asyncio.run(main())

