from .behaviors.core import BaseDocument
from .behaviors.timestamps import Timestamping


class Document(BaseDocument, Timestamping):
    pass
