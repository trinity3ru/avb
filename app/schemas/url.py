from pydantic import BaseModel, HttpUrl, ConfigDict


class ShortenRequest(BaseModel):
    url: HttpUrl

    model_config = ConfigDict(from_attributes=True)
