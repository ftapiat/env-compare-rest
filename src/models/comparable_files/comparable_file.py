from typing import Optional


class ComparableFile:
    def __init__(self, name: Optional[str], content: str, default_name: Optional[str] = None):
        self.name = name or default_name
        self.content = content
