from .comparable_file import ComparableFile


class UploadedFiles(object):
    def __init__(self, json_files):
        self.file_1 = ComparableFile(json_files[0])
        self.file_2 = ComparableFile(json_files[1])

    @property
    def serialized(self):
        return {
            "file_1": self.file_1.serialized,
            "file_2": self.file_2.serialized
        }
