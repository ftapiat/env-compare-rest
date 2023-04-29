from .comparable_file import ComparableFile

class UploadedFiles(object):
     def __init__(self, json_files):
         self.file_1 = ComparableFile(json_files[0])
         self.file_2 = ComparableFile(json_files[1])
