from enum import Enum

class DBMode(Enum):
    MONGO = "MongoDB"
    SQLITE = "SQLite"

ENCODING_FORMAT = "utf-8"
text_label_size = 25
text_subtitle_size = 18
input_field_width = 300