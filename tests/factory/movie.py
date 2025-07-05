from polyfactory.factories.pydantic_factory import ModelFactory
from app.core.domain.movie.dto import MovieDTO


class MovieDTOFactory(ModelFactory[MovieDTO]): ...
