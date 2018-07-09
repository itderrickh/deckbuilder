from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, TypeDecorator, VARCHAR
import json

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

Base = declarative_base()