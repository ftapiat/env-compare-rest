class AppResponse(object):
     def __init__(self, data):
         self.data = data

     @property
     def serialized(self):
        return {
            "data": self.data,
        }
