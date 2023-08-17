from pydantic import BaseModel
from typing import List


class Diagram(BaseModel):

    Verbs: List[str]
    Nouns: List[str]
