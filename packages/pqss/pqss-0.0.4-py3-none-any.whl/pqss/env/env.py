

class Environment:
    def __init__(self):
        self.parent: Environment | None = None
        self.store = {}  # id-val, id-mixin

    def get(self, name: str):
        obj = None
        if self.parent:
            obj = self.store.get(name)

        obj0 = self.store.get(name)

        return obj0 if obj0 else obj

    def set(self, name: str, val):
        self.store[name] = val
        return val
