from datetime import datetime
from typing import Callable

import asyncio
import functools

class AsyncEvents:
    def __init__(self) -> None:
        self.events = []
        self.time = datetime.now()
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        self.loop = loop
    
    def on_time_changed(self, change_type: str = "seconds") -> Callable:
        def decorator(func: Callable) -> Callable:
            self.events.append({"func": func, "type": change_type})
            @functools.wraps(func)
            async def wrapped(*args):
                return await func(*args)
            
            return wrapped

        return decorator
    
    async def process_event(self):
        while True:
            time = datetime.now()
            for i in self.events:
                if (i['type'] in ["ms", "microseconds"]) and (time.microsecond != self.time.microsecond):
                        try:
                            await self.loop.run_in_executor(
                                None,
                                func=lambda: self.loop.create_task(i['func'](time))
                            )
                        except:
                            pass

                elif (i['type'] in ["s", "seconds"]) and (time.second != self.time.second):
                        try:
                            await self.loop.run_in_executor(
                                None,
                                func=lambda: self.loop.create_task(i['func'](time))
                            )
                        except:
                            pass
                elif (i['type'] in ["m", "minutes"]) and (time.minute != self.time.minute):
                        try:
                            await self.loop.run_in_executor(
                                None,
                                func=lambda: self.loop.create_task(i['func'](time))
                            )
                        except:
                            pass

                elif (i['type'] in ["h", "hours"]) and (time.hour != self.time.hour):
                        try:
                            await self.loop.run_in_executor(
                                None,
                                func=lambda: self.loop.create_task(i['func'](time))
                            )
                        except:
                            pass
            
            self.time = time

    def run_forever(self):
        self.loop.create_task(self.process_event())
        self.loop.run_forever()

events = AsyncEvents()

@events.on_time_changed(change_type="seconds")
async def on_time(time: datetime):
    print(time)

@events.on_time_changed(change_type="minutes")
async def on_time2(time: datetime):
    print(time, "minute changed")

@events.on_time_changed(change_type="seconds")
def on_time3(time: datetime):
    print(time)

events.run_forever()
