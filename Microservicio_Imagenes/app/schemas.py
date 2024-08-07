from pydantic import BaseModel
from datetime import datetime

class ImageSchema(BaseModel):
    id: int
    filename: str
    upload_time: datetime

class ImageResponse(ImageSchema):
    pass