import copy

class DefaultDict (dict):
    """Dictionary with a default value for unknown keys."""
    def __init__(self, default):
        self.default = default
    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, copy.deepcopy(self.default))
    def sorted(self, rev=True):
        counts = [ (c,w) for w,c in self.items() ]
        counts.sort(reverse=rev)
        return counts

class CountingDict (DefaultDict):
    def __init__(self):
        DefaultDict.__init__(self, 0)

