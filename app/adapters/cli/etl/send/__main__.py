import click
from elasticsearch import Elasticsearch
from redis import Redis
import time
from app.core.domain.movie.command import (
    SendMovieToElasticSearchCommand,
)
from app.core.domain.movie.query import GetMoviesFromQueueQuery
from app.core.storage.rdb_impl import RedisQueue, RedisStorage
from app.storages.rdb.settings import settings as rdb_settings
from app.storages.elastic.settings import settings as elastic_settings


@click.command()
def main() -> None:
    redis = Redis.from_url(rdb_settings.url)
    get_movies_query: GetMoviesFromQueueQuery = GetMoviesFromQueueQuery(
        queue=RedisQueue(
            redis=redis,
        ),
        storage=RedisStorage(
            redis=redis,
        ),
    )
    send_command: SendMovieToElasticSearchCommand = SendMovieToElasticSearchCommand(
        client=Elasticsearch(
            hosts=elastic_settings.url,
            headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8"},
        )
    )
    while True:
        movies = get_movies_query.execute()
        send_command.process(value=movies)
        time.sleep(5)


if __name__ == "__main__":
    main()
