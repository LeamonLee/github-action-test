import datetime
import threading

def convertTmFields2String(data:dict):
    newData = data.copy()
    for k,v in data.items():
        if isinstance(v, datetime.datetime):
            newData[k] = v.strftime('%Y-%m-%dT%H:%M:%S')
    return newData
class MyInterval(threading.Thread):
    def __init__(self, func, interval, event):
        threading.Thread.__init__(self)
        self.stoppedEvent = event
        self.func = func
        self.interval = interval
        self.daemon = True

    def run(self):
        while not self.stoppedEvent.wait(self.interval):
            self.func()

    def cancel(self):
      self.stoppedEvent.set()