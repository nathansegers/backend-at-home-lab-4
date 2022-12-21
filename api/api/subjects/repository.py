from typing import List
from uuid import uuid4
from nosql_database import (
    get_database
)
from .models import Subject
import traceback
collection = get_database('subjects')

class SubjectRepository():

    @staticmethod
    def get_all() -> List[Subject]:
        try:
            subjects = collection.find()
            return [Subject(**document) for document in subjects]
        except Exception as err:
            print(traceback.format_exc())
            print(err)
            return []

    @staticmethod
    def create(subject: Subject) -> str:
        """Create a new book"""
        document = subject.dict()
        document["_id"] = str(uuid4())
        result = collection.insert_one(document)
        assert result.acknowledged
        return "Created"