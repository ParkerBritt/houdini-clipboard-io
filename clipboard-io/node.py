import os

class Node():
    def __init__(self, path: str):
        self.path = path
        self.name = os.path.splitext(os.path.split(self.path)[1])[0]

    def __str__(self):
        return "NODE:"+self.name

    def __repr__(self):
        return "NODE:"+self.name

