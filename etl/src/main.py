import elasticsearch
import psycopg2
from config import BODY_FILM, BODY_GENRE, BODY_PERSON, DSL, EL_DSL, INDEX_FILM, INDEX_GENRE, INDEX_PERSON, LIMIT_ROWS
from scheme.film import Movie
from scheme.genre import Genre
from scheme.person import Person
from service import backoff
from state import JsonFileStorage, State

from etl import DataTransformer, ElasticsearchLoader, PostgresExtractor


@backoff()
def main():
    entities = {
        "film": {"scheme": Movie, "index_name": INDEX_FILM, "body": BODY_FILM},
        "genre": {"scheme": Genre, "index_name": INDEX_GENRE, "body": BODY_GENRE},
        "person": {"scheme": Person, "index_name": INDEX_PERSON, "body": BODY_PERSON},
    }

    with psycopg2.connect(**DSL) as pg_conn, elasticsearch.Elasticsearch(**EL_DSL) as es:
        pg_client = PostgresExtractor(pg_conn)
        es_client = ElasticsearchLoader(es)

        for entity in entities.values():
            es_client.create_mapping(index_name=entity["index_name"], body=entity["body"])

        storage = JsonFileStorage("data.json")
        state = State(storage)

        while True:
            current_timestamp = pg_client.get_now()

            from_date = state.get_state("film_modified")
            step_pg = state.get_state("film_step_pg")
            data_movies = pg_client.get_chunk_movies(from_date=from_date, limit=LIMIT_ROWS, step=step_pg)
            data_tran_movie = DataTransformer(data_movies, Movie, INDEX_FILM).transform()
            data_load_movie = es_client.bulk_index_offers(data_tran_movie)

            if len(data_load_movie):
                step_pg += 1
                state.set_state("film_step_pg", step_pg)
            else:
                state.set_state("film_step_pg", 0)
                state.set_state("film_modified", current_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f%z"))
                break

            from_date = state.get_state("genre_modified")
            step_pg = state.get_state("genre_step_pg")

            data_genre = pg_client.get_chunk_genre(from_date=from_date, limit=LIMIT_ROWS, step=step_pg)
            data_tran_genre = DataTransformer(data_genre, Genre, INDEX_GENRE).transform()
            data_load_genre = es_client.bulk_index_offers(data_tran_genre)
            if len(data_load_genre):
                step_pg += 1
                state.set_state("genre_step_pg", step_pg)
            else:
                state.set_state("genre_step_pg", 0)
                state.set_state("genre_modified", current_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f%z"))
                break

            from_date = state.get_state("person_modified")
            step_pg = state.get_state("person_step_pg")

            data_person = pg_client.get_chunk_person(from_date=from_date, limit=LIMIT_ROWS, step=step_pg)

            data_tran_person = DataTransformer(data_person, Person, INDEX_PERSON).transform()
            data_load_person = es_client.bulk_index_offers(data_tran_person)

            if len(data_load_person):
                step_pg += 1
                state.set_state("person_step_pg", step_pg)
            else:
                state.set_state("person_step_pg", 0)
                state.set_state("person_modified", current_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f%z"))
                break


if __name__ == "__main__":
    main()
