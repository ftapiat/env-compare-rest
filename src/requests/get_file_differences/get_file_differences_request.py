from src.models.comparable_files.comparable_file import ComparableFile


class GetFileDifferencesRequest:
    def __init__(self, files: list[ComparableFile]):
        self.files = files

    @property
    def file_1(self):
        return self.files[0]

    @property
    def file_2(self):
        return self.files[1]
