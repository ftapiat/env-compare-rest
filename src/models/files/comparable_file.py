class ComparableFile(object):
     def __init__(self, file):
         self.name = file["name"]
         self.content = file["content"]

     @property
     def serialized(self):
        return {
            "name": self.name,
            "content": self.content
        }
