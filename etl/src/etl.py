from typing import Generator, List

import datetime
import json

from config import logger
from elasticsearch import Elasticsearch, helpers
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, DictRow, RealDictCursor, RealDictRow
from pydantic import ValidationError


class PostgresExtractor:
    """Получаем данные из базы Postgres."""

    def __init__(self, conn: _connection) -> None:
        self._connection = conn
        self.dict_cursor: DictCursor = self._connection.cursor(cursor_factory=DictCursor)
        self.real_cursor: RealDictCursor = self._connection.cursor(cursor_factory=RealDictCursor)

    def get_now(
        self,
    ) -> DictRow:
        self.dict_cursor.execute(f"""SELECT now() as date;""")
        return self.dict_cursor.fetchone()["date"]

    def get_last_timestamp(
        self,
    ) -> DictRow:
        sql = f"""SELECT fw.modified as date
                     FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                    GROUP BY fw.id
                    ORDER BY fw.modified
                    LIMIT 1"""
        self.dict_cursor.execute(sql)
        return self.dict_cursor.fetchone()["date"]

    def get_chunk_movies(self, from_date: datetime, limit: int = 100, step: int = 0) -> List[RealDictRow]:
        self.real_cursor.execute(
            f"""
                    SELECT
                    fw.id,
                    fw.title,
                    fw.description,
                    fw.rating as rating,
                    ARRAY_AGG(DISTINCT g.name) as genre,
                    ARRAY_AGG(DISTINCT p.full_name)
                    FILTER(WHERE pfw.role = 'director') AS director,
                    ARRAY_AGG(DISTINCT p.full_name)
                    FILTER(WHERE pfw.role = 'actor') AS actors_names,
                    ARRAY_AGG(DISTINCT p.full_name)
                    FILTER(WHERE pfw.role = 'writer') AS writers_names,                
                    COALESCE (JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) 
                    FILTER(WHERE pfw.role = 'actor'), '[]') AS actors,
                    COALESCE (JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) 
                    FILTER(WHERE pfw.role = 'writer'), '[]') AS writers
                    FROM content.film_work fw
                    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                    LEFT JOIN content.person p ON p.id = pfw.person_id
                    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                    LEFT JOIN content.genre g ON g.id = gfw.genre_id
                    WHERE (
                    fw.modified>= '{from_date}'
                    )
                    GROUP BY fw.id
                    ORDER BY fw.modified
                    LIMIT {limit} offset {step * limit}
                            """
        )
        rows: List[RealDictRow] = self.real_cursor.fetchall()
        return rows

    def get_chunk_genre(self, from_date: datetime, limit: int = 100, step: int = 0) -> List[RealDictRow]:
        self.real_cursor.execute(
            f"""
                    SELECT
                    g.id,
                    g.name,
                    g.description
                    FROM content.genre g
                    WHERE
                    g.modified>= '{from_date}'
                    and g.id in (SELECT g.id FROM content.genre_film_work)
                    ORDER BY g.modified
                    LIMIT {limit} offset {step * limit}
                            """
        )
        rows: List[RealDictRow] = self.real_cursor.fetchall()
        return rows

    def get_chunk_person(self, from_date: datetime, limit: int = 100, step: int = 0) -> List[RealDictRow]:
        self.real_cursor.execute(
            f"""
                    SELECT
                    p.id,
                    p.full_name
                    FROM content.person p
                    WHERE 
                    p.modified>= '{from_date}'                   
                    and p.id in (SELECT p.id FROM content.person_film_work)
                    ORDER BY p.modified
                    LIMIT {limit} offset {step * limit}
                            """
        )
        rows: List[RealDictRow] = self.real_cursor.fetchall()
        return rows


class DataTransformer:
    """Сырые данные из Postgres преобразует в формат пригодный для записи Elasticsearch."""

    def __init__(self, data, scheme, index_name) -> None:
        self.validation_data = data
        self.scheme = scheme
        self.index_name = index_name

    def validate(self, data):
        return self.scheme.parse_raw(json.dumps(data)).dict()

    def transform(self) -> Generator:
        try:
            for row in self.validation_data:
                yield {"_index": self.index_name, "_id": self.validate(row)["id"], "_source": self.validate(row)}
        except ValidationError as err:
            logger.error(err)


class ElasticsearchLoader:
    """Класс забирает данные в подготовленном формате и загружает их в Elasticsearch."""

    def __init__(self, conn: Elasticsearch) -> None:
        self.es = conn

    def create_mapping(self, index_name, body):
        """create an index with the defined mapping - no documents added"""
        if not self.es.indices.exists(index_name):
            resp = self.es.indices.create(index=index_name, body=body)

    def bulk_index_offers(self, data):
        resp = helpers.bulk(self.es, data, request_timeout=3600)
        return resp
