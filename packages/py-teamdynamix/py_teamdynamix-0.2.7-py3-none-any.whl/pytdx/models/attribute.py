from typing import Optional, List
from .base_model import BaseModel


class AttributeChoice(BaseModel):
    def __init__(
        self,
        ID: Optional[int] = None,
        Name: Optional[str] = None,
        IsActive: Optional[bool] = None,
        DateCreated: Optional[str] = None,
        DateModified: Optional[str] = None,
        Order: Optional[int] = None,
    ):
        self.ID = ID
        self.Name = Name
        self.IsActive = IsActive
        self.DateCreated = DateCreated
        self.DateModified = DateModified
        self.Order = Order
