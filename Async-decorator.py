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
        except:
            loop = asyncio.new_event_loop()
        
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
            funcs = []
            if time.second != self.time.second:
                for i in self.events:
                    if i["type"] in ["s", "seconds"]:
                        funcs.append(i['func'](time))
        
            if time.minute != self.time.minute:
                for i in self.events:
                    if i["type"] in ["m", "minutes"]:
                        funcs.append(i['func'](time))
        
            if time.hour != self.time.hour:
                for i in self.events:
                    if i["type"] in ["h", "hours"]:
                        funcs.append(i['func'](time))

            self.time = time
            await self.loop.create_task(self.__run(funcs))

    async def __run(self, funcs):
        await asyncio.gather(*funcs)

    def start(self):
        self.loop.run_until_complete(self.process_event())

events = AsyncEvents()

@events.on_time_changed(change_type="seconds")
async def on_time(time: datetime):
    print(time)

@events.on_time_changed(change_type="minutes")
async def on_time2(time: datetime):
    print(time, "minute changed")

events.start()