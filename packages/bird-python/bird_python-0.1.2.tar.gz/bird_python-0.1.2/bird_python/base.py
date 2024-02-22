

class Base:
    def load(self, data):
        if data is not None:
            for name, value in list(data.items()):
                if hasattr(self, name) and not callable(getattr(self, name)):
                    setattr(self, name, value)

        return self
