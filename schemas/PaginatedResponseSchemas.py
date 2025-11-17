from pydantic import BaseModel
from typing import List, Optional, Generic, TypeVar


T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """
    A generic Pydantic model for paginated responses.
    `data` will be a list of items of type T.
    `total` will be the total count of items.
    """
    data: List[T]
    total: int

