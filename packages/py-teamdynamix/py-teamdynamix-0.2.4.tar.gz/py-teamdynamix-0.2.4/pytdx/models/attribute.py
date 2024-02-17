from typing import Optional, List


class BaseClass:
    def to_dict(self):
        return {key: value for key, value in vars(self).items() if value is not None}


class AttributeChoice(BaseClass):
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
