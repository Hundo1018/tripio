import asyncio
import queue
import threading
from typing import Any, Optional, Union
import serial_asyncio


class IoLoopMeta(type):
    """
    This will create a EventLoop-ThreadPool pair out of Main-Thread once and only once

    life time follow the last of task
    """

    _thread = None
    _loop = None
    _lock = threading.Lock()
    recv_queue: queue.Queue[bytes]

    def __call__(cls, *args: Any, **kwargs: Any):
        cls.recv_queue: queue.Queue[bytes]
        # 確保 thread 只建一次
        with cls._lock:
            if cls._thread is None:
                # 建 thread
                cls._loop = asyncio.new_event_loop()
                cls._thread = threading.Thread(
                    target=cls._start_loop,
                    args=(cls._loop,),
                    daemon=True,
                    name="IoLoop",
                )
                cls._thread.start()
        # 返回正常 class 實例
        return super().__call__(*args, **kwargs)

    @staticmethod
    def _start_loop(loop: asyncio.AbstractEventLoop):
        asyncio.set_event_loop(loop)
        loop.run_forever()


class Tripio(metaclass=IoLoopMeta):
    class SerialProtocol(asyncio.Protocol):
        def connection_made(self, transport: asyncio.BaseTransport) -> None:
            print("serialport opened:", transport)
            return super().connection_made(transport)

        def data_received(self, data: bytes):
            print("data received:", data.decode().strip())

        def eof_received(self):
            print("got eof")

        def connection_lost(self, exc: Optional[Exception]):
            print("serial port closed")

    def open(self, port: str, baud: int):
        coro = serial_asyncio.create_serial_connection(
            self._loop, Tripio.SerialProtocol, port, baud
        )
        task = self._loop.create_task(coro)
        f = asyncio.run_coroutine_threadsafe(coro, type(self)._loop)
        return f

    def close(self): ...


def main():
    t = Tripio()
    task = t.open("COM5", 115200)
    task2 = t.open("COM3", 115200)
    print(task, task2)


main()
