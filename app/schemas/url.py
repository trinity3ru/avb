from pydantic import BaseModel, ConfigDict, HttpUrl


class ShortenRequest(BaseModel):
    url: HttpUrl

    model_config = ConfigDict(from_attributes=True)
