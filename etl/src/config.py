import logging
import os

# Конфигурация логов
logging.basicConfig(
    filename="ETL.log", level=logging.DEBUG, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)
logger = logging.getLogger()

LIMIT_ROWS = 100

# Конфигурация для доступа к БД Postgresql
DSL = {
    "dbname": os.environ.get("DB_NAME", "movies_database"),
    "user": os.environ.get("DB_USER", "app"),
    "password": os.environ.get("DB_PASSWORD", "123qwe"),
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "port": os.environ.get("DB_PORT", ""),
}

# Конфигурация для доступа к БД Elasticsearch
EL_DSL = {
    "hosts": [
        "http://{}:{}".format(os.environ.get("ELASTIC_HOST", "127.0.0.1"), os.environ.get("ELASTIC_PORT", "9200"))
    ],
    "basic_auth": (os.environ.get("ELASTIC_USER"), os.environ.get("ELASTIC_PASSWORD")),
}

INDEX_FILM = "movies"
INDEX_GENRE = "genre"
INDEX_PERSON = "person"

BODY_FILM = {
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {"type": "stemmer", "language": "possessive_english"},
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                }
            },
        },
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "imdb_rating": {"type": "float"},
            "genre": {"type": "keyword"},
            "title": {"type": "text", "analyzer": "ru_en", "fields": {"raw": {"type": "keyword"}}},
            "description": {"type": "text", "analyzer": "ru_en"},
            "director": {"type": "text", "analyzer": "ru_en"},
            "actors_names": {"type": "text", "analyzer": "ru_en"},
            "writers_names": {"type": "text", "analyzer": "ru_en"},
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {"id": {"type": "keyword"}, "name": {"type": "text", "analyzer": "ru_en"}},
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {"id": {"type": "keyword"}, "name": {"type": "text", "analyzer": "ru_en"}},
            },
        },
    },
}

BODY_GENRE = {
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {"type": "stemmer", "language": "possessive_english"},
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                }
            },
        },
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "name": {"type": "text", "analyzer": "ru_en", "fields": {"raw": {"type": "keyword"}}},
            "description": {"type": "text", "analyzer": "ru_en"},
        },
    },
}

BODY_PERSON = {
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {"type": "stemmer", "language": "possessive_english"},
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                }
            },
        },
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "name": {"type": "text", "analyzer": "ru_en", "fields": {"raw": {"type": "keyword"}}},
        },
    },
}
