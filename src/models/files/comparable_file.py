class ComparableFile:
    def __init__(self, file, default_name=None):
        self.name = file["name"] or default_name
        self.content = file["content"]

    @property
    def serialized(self):
        return {
            "name": self.name,
            "content": self.content
        }
