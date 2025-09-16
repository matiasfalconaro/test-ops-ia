from enum import Enum

class ExtractType(str, Enum):
    TEXT = "text"
    ATTRIBUTE = "attribute"
    HTML = "html"
