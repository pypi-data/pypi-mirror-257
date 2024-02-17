from typing import Optional, List
from .base_model import BaseModel


class Attribute(BaseModel):
    def __init__(
        self,
        ID: Optional[int] = None,
        Name: Optional[str] = None,
        Order: Optional[int] = None,
        Description: Optional[str] = None,
        SectionID: Optional[int] = None,
        SectionName: Optional[str] = None,
        FieldType: Optional[str] = None,
        DataType: Optional[str] = None,
        Choices: Optional[List[str]] = None,
        IsRequired: Optional[bool] = None,
        IsUpdatable: Optional[bool] = None,
        Value: Optional[str] = None,
        ValueText: Optional[str] = None,
        ChoicesText: Optional[str] = None,
        AssociatedItemIDs: Optional[List[int]] = None,
    ):
        self.ID = ID
        self.Name = Name
        self.Order = Order
        self.Description = Description
        self.SectionID = SectionID
        self.SectionName = SectionName
        self.FieldType = FieldType
        self.DataType = DataType
        self.Choices = Choices
        self.IsRequired = IsRequired
        self.IsUpdatable = IsUpdatable
        self.Value = Value
        self.ValueText = ValueText
        self.ChoicesText = ChoicesText
        self.AssociatedItemIDs = AssociatedItemIDs


class KnowledgeArticle(BaseModel):
    def __init__(
        self,
        ID: Optional[int] = None,
        AppID: Optional[int] = None,
        AppName: Optional[str] = None,
        CategoryID: Optional[int] = None,
        CategoryName: Optional[str] = None,
        Subject: Optional[str] = None,
        Body: Optional[str] = None,
        Summary: Optional[str] = None,
        Status: Optional[int] = None,
        Attributes: Optional[List[Attribute]] = None,
        ReviewDateUtc: Optional[str] = None,
        Order: Optional[float] = None,
        IsPublished: Optional[bool] = None,
        IsPublic: Optional[bool] = None,
        WhitelistGroups: Optional[bool] = None,
        InheritPermissions: Optional[bool] = None,
        NotifyOwner: Optional[bool] = None,
        RevisionID: Optional[int] = None,
        RevisionNumber: Optional[int] = None,
        DraftStatus: Optional[str] = None,
        CreatedDate: Optional[str] = None,
        CreatedUid: Optional[str] = None,
        CreatedFullName: Optional[str] = None,
        ModifiedDate: Optional[str] = None,
        ModifiedUid: Optional[str] = None,
        ModifiedFullName: Optional[str] = None,
        OwnerUid: Optional[str] = None,
        OwnerFullName: Optional[str] = None,
        OwningGroupID: Optional[int] = None,
        OwningGroupName: Optional[str] = None,
        Tags: Optional[List[str]] = None,
        Attachments: Optional[List[str]] = None,
        Uri: Optional[str] = None,
    ):
        self.ID = ID
        self.AppID = AppID
        self.AppName = AppName
        self.CategoryID = CategoryID
        self.CategoryName = CategoryName
        self.Subject = Subject
        self.Body = Body
        self.Summary = Summary
        self.Status = Status
        self.Attributes = Attributes
        self.ReviewDateUtc = ReviewDateUtc
        self.Order = Order
        self.IsPublished = IsPublished
        self.IsPublic = IsPublic
        self.WhitelistGroups = WhitelistGroups
        self.InheritPermissions = InheritPermissions
        self.NotifyOwner = NotifyOwner
        self.RevisionID = RevisionID
        self.RevisionNumber = RevisionNumber
        self.DraftStatus = DraftStatus
        self.CreatedDate = CreatedDate
        self.CreatedUid = CreatedUid
        self.CreatedFullName = CreatedFullName
        self.ModifiedDate = ModifiedDate
        self.ModifiedUid = ModifiedUid
        self.ModifiedFullName = ModifiedFullName
        self.OwnerUid = OwnerUid
        self.OwnerFullName = OwnerFullName
        self.OwningGroupID = OwningGroupID
        self.OwningGroupName = OwningGroupName
        self.Tags = Tags
        self.Attachments = Attachments
        self.Uri = Uri
