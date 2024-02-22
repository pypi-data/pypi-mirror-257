import json

from bson import ObjectId

from redbaby.behaviors.objectids import ObjectIdDoc
from redbaby.pyobjectid import PyObjectId


class TDoc1(ObjectIdDoc):
    attr: int


def test_id_use():
    doc = TDoc1(attr=1)
    assert doc.id is not None
    assert isinstance(doc.id, PyObjectId)
    assert len(str(doc.id)) == 24
    dumped = doc.model_dump(by_alias=True)
    assert dumped["_id"] == doc.id
    # TODO model_dump mode=python should output ObjectId, not str
    from_dumped = TDoc1(**dumped)
    assert from_dumped.id == doc.id


def test_json_dumps_str():
    doc = TDoc1(attr=1)
    dumped = doc.model_dump_json(by_alias=True)
    dict_dumped = json.loads(dumped)
    assert isinstance(dict_dumped["_id"], str)
    assert dict_dumped["_id"] == str(doc.id)
