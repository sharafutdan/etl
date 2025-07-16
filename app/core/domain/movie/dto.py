import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Annotated, Any
import json


class FilmParticipantDTO(BaseModel):
    id: Annotated[UUID, Field(...)]
    name: Annotated[str, Field(...)]


class MovieDTO(BaseModel):
    id: Annotated[
        UUID,
        Field(
            ...,
        ),
    ]
    title: Annotated[str, Field(...)]
    description: Annotated[str | None, Field(...)]
    imdb_rating: Annotated[float | None, Field(...)]
    genres: Annotated[list[str], Field(...)]
    directors_names: Annotated[list[str], Field(...)]
    actors_names: Annotated[list[str], Field(...)]
    writers_names: Annotated[list[str], Field(...)]
    directors: Annotated[list[FilmParticipantDTO], Field(...)]
    actors: Annotated[list[FilmParticipantDTO], Field(...)]
    writers: Annotated[list[FilmParticipantDTO], Field(...)]

    def serialize(self):
        return json.dumps(self.model_dump(mode="json", by_alias=True))

    @property
    def key(self) -> str:
        return f"movie:{self.id}"


class FilmWorkDTO(BaseModel):
    id: Annotated[UUID, Field(...)]
    title: Annotated[str, Field(...)]
    description: Annotated[str, Field(...)]
    created_at: Annotated[datetime.datetime, Field(..., alias="creation_date")]
    imdb_rating: Annotated[float, Field(..., alias="rating")]
    type: Annotated[str, Field(...)]
    updated_at: Annotated[datetime.datetime, Field(..., alias="modified")]

    @property
    def as_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="python", by_alias=True)
