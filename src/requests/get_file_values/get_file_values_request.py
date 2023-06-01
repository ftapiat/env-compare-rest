class GetFileValuesRequestFile:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


class GetFileValuesRequest:
    def __init__(self, file: GetFileValuesRequestFile):
        self.file = file
