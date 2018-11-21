import threading, time, os

class Cache():
    def __init__(self, maxTime, interval, path = "__cache"):
        global lock
        self.map = {}
        self.path = path
        self.monitoring = True
        self.monitor = threading.Thread(target = self.trim)
        if not os.path.exists(path):
            os.makedirs(path)
    def __setitem__(self, key, value):
        self.map[hash(key)]["access"] = time.tome
        self.map[hash(key)]["data"] = value
        return hash(key)
    def __getitem__(self, key):
        return self.map[hash(key)]
    def __delitem__(self, key):
        del self.map[hash(key)]
    def __repr__(self):
        return self.map
        # todo non time
    def trim(self):
        sortedArray = sorted([x for x in self.map], key = lambda x : self.map[x]["access"])
        index = self.binarySearchBetween(self.maxTime, sortedArray)
        if index < 0:
            return
        for i in sortedArray[index:]:
            del self.map[i]
    def binarySearchBetween(key, array):
        min = 0
        max = len(array) - 1
        while True:
            index = (max + min) // 2
            if array[index] >= key:
                if array[index - 1] < key:
                    return index
                max = index
            if array[index] <= key:
                if array[index + 1] > key:
                    return index
                min = index + 1
            if min >= max:
                return -1
    def monitor(self, interval = 120):
        while self.monitoring:
            time.sleep(interval)
            self.trim()
    def toggleMonitoring(self):
        self.monitoring = not self.monitoring

class Server():
    def __init__(self):
        self.map = {}
    def bind(self, server, object, bind):
        if not hasattr(object, "id"):
            raise TypeError("Object has no id")
        self.map[server][bind] = object
    def get(self, server, bind):
        if server not in self.map:
            return None
        try:
            return self.map[server][bind]
        except:
            return None
    def delete(self, server, bind):
        if bind not in self.map[server]:
            raise IndexError
        del self.map[server][bind]
    def initServer(self, server, channel, colors):
        self.map[server] = {
            "bot": channel,
            "color":{
                **colors
            }
        }
    def setColor(self, server, status, color):
        self.map[server]["color"][status] = color
    def color(self, server, status = "normal"):
        return self.map[server]["color"][status]
    def colorTypes(self, server):
        return [x for x in self.map[server]["color"]]
