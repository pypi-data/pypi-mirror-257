from typing import List, Optional


class BaseClass:
    def to_dict(self):
        return {key: value for key, value in vars(self).items() if value is not None}


class Attribute(BaseClass):
    def __init__(
        self,
        ID=None,
        Name=None,
        Order=None,
        Description=None,
        SectionID=None,
        SectionName=None,
        FieldType=None,
        DataType=None,
        Choices=None,
        IsRequired=None,
        IsUpdatable=None,
        Value=None,
        ValueText=None,
        ChoicesText=None,
        AssociatedItemIDs=None,
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


class KnowledgeArticle(BaseClass):
    def __init__(
        self,
        ID=None,
        AppID=None,
        AppName=None,
        CategoryID=None,
        CategoryName=None,
        Subject=None,
        Body=None,
        Summary=None,
        Status=None,
        Attributes=None,
        ReviewDateUtc=None,
        Order=None,
        IsPublished=None,
        IsPublic=None,
        WhitelistGroups=None,
        InheritPermissions=None,
        NotifyOwner=None,
        RevisionID=None,
        RevisionNumber=None,
        DraftStatus=None,
        CreatedDate=None,
        CreatedUid=None,
        CreatedFullName=None,
        ModifiedDate=None,
        ModifiedUid=None,
        ModifiedFullName=None,
        OwnerUid=None,
        OwnerFullName=None,
        OwningGroupID=None,
        OwningGroupName=None,
        Tags=None,
        Attachments=None,
        Uri=None,
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
        self.Attributes = (
            [Attribute(**attr) for attr in Attributes] if Attributes else None
        )
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
