from sqlalchemy import create_engine, String, TypeDecorator, VARCHAR
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch
import json

Engine = create_engine('sqlite:///deck_builder.db', connect_args={'check_same_thread': False})

Session = sessionmaker(bind=Engine)
ElasticStore = Elasticsearch()
ses = Session()

class JSONType(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value, use_decimal=True)

    def process_result_value(self, value, dialect):
        if not value:
            return None
        return json.loads(value, use_decimal=True)