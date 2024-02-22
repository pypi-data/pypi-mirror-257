import json

from pydantic import TypeAdapter

from redbaby.behaviors.hashids import HashIdDoc
from redbaby.hashing import HashDigest


class TDoc1(HashIdDoc):
    attr: int

    def hashable_fields(self) -> list[str]:
        return [str(self.attr)]


def test_id_use():
    doc = TDoc1(attr=1)
    assert doc.id is not None
    ta = TypeAdapter(HashDigest)
    assert ta.validate_python(doc.id)
    assert len(str(doc.id)) == 42
    dumped = doc.model_dump(by_alias=True)
    assert dumped["_id"] == doc.id
    from_dumped = TDoc1(**dumped)
    assert from_dumped.id == doc.id
    construct_model = TDoc1.model_construct(**dumped, ass=1)
    assert construct_model.id == doc.id
    assert TDoc1(attr=2).id != doc.id
    # TODO: find a way to avoid recalculating the hash everytime
