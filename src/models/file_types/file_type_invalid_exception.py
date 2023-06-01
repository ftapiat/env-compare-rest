class FileTypeInvalidException(Exception):
    def __init__(self):
        message = "Invalid file type."
        self.message = message
        print(message)
