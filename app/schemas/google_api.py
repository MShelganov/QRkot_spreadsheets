from pydantic import BaseModel, Field, HttpUrl

from app.services import constants as const


class GoogleApiReport(BaseModel):
    url: HttpUrl = Field(
        ...,
        example=const.GOOGLE_API_EXAMPLE
    )
