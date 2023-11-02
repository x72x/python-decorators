from datetime import datetime
from typing import Callable
from threading import Thread

class Events:
    def __init__(self) -> None:
        self.events = []
        self.time = datetime.now()
    
    def on_time_changed(self, change_type: str = "seconds") -> Callable:
        def decorator(func: Callable) -> Callable:
            self.events.append({"func": func, "type": change_type})

        return decorator
    
    def process_event(self, time: datetime):
        if time.second != self.time.second:
            for i in self.events:
                if i["type"] in ["s", "seconds"]:
                    Thread(target=i['func'], args=(time,)).start()
        
        if time.minute != self.time.minute:
            for i in self.events:
                if i["type"] in ["m", "minutes"]:
                    Thread(target=i['func'], args=(time,)).start()
        
        if time.hour != self.time.hour:
            for i in self.events:
                if i["type"] in ["h", "hours"]:
                    Thread(target=i['func'], args=(time,)).start()

        self.time = time

    def start(self):
        print(len(self.events))
        while True:
            self.process_event(datetime.now())

events = Events()

@events.on_time_changed(change_type="s")
def on_time(time: datetime):
    print(time)

@events.on_time_changed(change_type="minutes")
def on_time2(time: datetime):
    print(time, "minute changed")

events.start()