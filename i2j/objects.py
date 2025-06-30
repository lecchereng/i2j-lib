import base64
import mimetypes
import asyncio
from typing import TypedDict

class ImageData:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = filepath.split("/")[-1]
        self.content_type = mimetypes.guess_type(filepath)[0] or "application/octet-stream"

    async def read(self):
        with open(self.filepath, "rb") as f:
            return f.read()
        
class ImageJson(TypedDict):
    filename: str
    content_type: str
    base64: str