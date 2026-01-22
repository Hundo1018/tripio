import asyncio
import queue
import random
import signal
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import time
from typing import Any
import serial_asyncio


class IoLoopMeta(type):
    """
    This will create a EventLoop-ThreadPool pair out of Main-Thread once and only once

    life time follow the last of task
    """

    global IoLoop
    _thread = None
    _loop = None
    _lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any):
        # 確保 thread 只建一次
        with cls._lock:
            if cls._thread is None:
                # 建 thread
                cls._loop = asyncio.new_event_loop()
                cls._thread = threading.Thread(
                    target=cls._start_loop, args=(cls._loop,), daemon=True
                )
                cls._thread.start()
        # 返回正常 class 實例
        return super().__call__(*args, **kwargs)

    @staticmethod
    def _start_loop(loop: asyncio.AbstractEventLoop):
        asyncio.set_event_loop(loop)
        loop.run_forever()


class SerialProtocol(asyncio.Protocol):
    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        print("serialport opened:", transport)
        return super().connection_made(transport)

    def data_received(self, data):
        print("data received:", data.decode().strip())

    def eof_received(self):
        print("got eof")

    def connection_lost(self, exc):
        print("serial port closed")


class Tripio(metaclass=IoLoopMeta):
    async def open_async(self, port, baud):
        loop = asyncio.get_running_loop()
        transport, port = await serial_asyncio.create_serial_connection(
            loop, SerialProtocol, port, baud
        )
        return transport

    def open(self, port, baud):
        loop = asyncio.get_event_loop()
        task = loop.create_task(
            serial_asyncio.create_serial_connection(
                loop, SerialProtocol, port, baud
            )
        )
        return loop.gather(task)


def main():
    t = Tripio()
    task = t.open("COM5", 115200)
    task2 = t.open("COM3", 115200)
    print(task, task2)


main()
