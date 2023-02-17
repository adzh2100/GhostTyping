class Score:
    def __init__(self, name, points):
        self._name = name
        self._points = points

    def get_points(self):
        return self._points

    def get_name(self):
        return self._name
