from typing import Optional, List, Dict
from .base_model import BaseModel


class Choice(BaseModel):
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
        IsRequired: Optional[bool] = None,
        IsUpdatable: Optional[bool] = None,
        Value: Optional[str] = None,
        ValueText: Optional[str] = None,
        ChoicesText: Optional[str] = None,
        AssociatedItemIDs: Optional[List[int]] = None,
        Choices: Optional[List[Choice]] = None,
    ):
        self.ID = ID
        self.Name = Name
        self.Order = Order
        self.Description = Description
        self.SectionID = SectionID
        self.SectionName = SectionName
        self.FieldType = FieldType
        self.DataType = DataType
        self.IsRequired = IsRequired
        self.IsUpdatable = IsUpdatable
        self.Value = Value
        self.ValueText = ValueText
        self.ChoicesText = ChoicesText
        self.AssociatedItemIDs = AssociatedItemIDs
        self.Choices = Choices


class Asset(BaseModel):
    def __init__(
        self,
        ID: Optional[int] = None,
        AppID: Optional[int] = None,
        AppName: Optional[str] = None,
        FormID: Optional[int] = None,
        FormName: Optional[str] = None,
        ProductModelID: Optional[int] = None,
        ProductModelName: Optional[str] = None,
        ManufacturerID: Optional[int] = None,
        ManufacturerName: Optional[str] = None,
        SupplierID: Optional[int] = None,
        SupplierName: Optional[str] = None,
        StatusID: Optional[int] = None,
        StatusName: Optional[str] = None,
        LocationID: Optional[int] = None,
        LocationName: Optional[str] = None,
        LocationRoomID: Optional[int] = None,
        LocationRoomName: Optional[str] = None,
        Tag: Optional[str] = None,
        SerialNumber: Optional[str] = None,
        Name: Optional[str] = None,
        PurchaseCost: Optional[float] = None,
        AcquisitionDate: Optional[str] = None,
        ExpectedReplacementDate: Optional[str] = None,
        RequestingCustomerID: Optional[str] = None,
        RequestingCustomerName: Optional[str] = None,
        RequestingDepartmentID: Optional[int] = None,
        RequestingDepartmentName: Optional[str] = None,
        OwningCustomerID: Optional[str] = None,
        OwningCustomerName: Optional[str] = None,
        OwningDepartmentID: Optional[int] = None,
        OwningDepartmentName: Optional[str] = None,
        ParentID: Optional[int] = None,
        ParentSerialNumber: Optional[str] = None,
        ParentName: Optional[str] = None,
        ParentTag: Optional[str] = None,
        MaintenanceScheduleID: Optional[int] = None,
        MaintenanceScheduleName: Optional[str] = None,
        ConfigurationItemID: Optional[int] = None,
        CreatedDate: Optional[str] = None,
        CreatedUid: Optional[str] = None,
        CreatedFullName: Optional[str] = None,
        ModifiedDate: Optional[str] = None,
        ModifiedUid: Optional[str] = None,
        ModifiedFullName: Optional[str] = None,
        ExternalID: Optional[str] = None,
        ExternalSourceID: Optional[int] = None,
        ExternalSourceName: Optional[str] = None,
        Attributes: Optional[List[Attribute]] = None,
        Attachments: Optional[List] = None,
        Uri: Optional[str] = None,
    ):
        self.ID = ID
        self.AppID = AppID
        self.AppName = AppName
        self.FormID = FormID
        self.FormName = FormName
        self.ProductModelID = ProductModelID
        self.ProductModelName = ProductModelName
        self.ManufacturerID = ManufacturerID
        self.ManufacturerName = ManufacturerName
        self.SupplierID = SupplierID
        self.SupplierName = SupplierName
        self.StatusID = StatusID
        self.StatusName = StatusName
        self.LocationID = LocationID
        self.LocationName = LocationName
        self.LocationRoomID = LocationRoomID
        self.LocationRoomName = LocationRoomName
        self.Tag = Tag
        self.SerialNumber = SerialNumber
        self.Name = Name
        self.PurchaseCost = PurchaseCost
        self.AcquisitionDate = AcquisitionDate
        self.ExpectedReplacementDate = ExpectedReplacementDate
        self.RequestingCustomerID = RequestingCustomerID
        self.RequestingCustomerName = RequestingCustomerName
        self.RequestingDepartmentID = RequestingDepartmentID
        self.RequestingDepartmentName = RequestingDepartmentName
        self.OwningCustomerID = OwningCustomerID
        self.OwningCustomerName = OwningCustomerName
        self.OwningDepartmentID = OwningDepartmentID
        self.OwningDepartmentName = OwningDepartmentName
        self.ParentID = ParentID
        self.ParentSerialNumber = ParentSerialNumber
        self.ParentName = ParentName
        self.ParentTag = ParentTag
        self.MaintenanceScheduleID = MaintenanceScheduleID
        self.MaintenanceScheduleName = MaintenanceScheduleName
        self.ConfigurationItemID = ConfigurationItemID
        self.CreatedDate = CreatedDate
        self.CreatedUid = CreatedUid
        self.CreatedFullName = CreatedFullName
        self.ModifiedDate = ModifiedDate
        self.ModifiedUid = ModifiedUid
        self.ModifiedFullName = ModifiedFullName
        self.ExternalID = ExternalID
        self.ExternalSourceID = ExternalSourceID
        self.ExternalSourceName = ExternalSourceName
        self.Attributes = Attributes
        self.Attachments = Attachments
        self.Uri = Uri


class AssetModel(BaseModel):
    def __init__(
        self,
        ID: Optional[int] = None,
        AppID: Optional[int] = None,
        AppName: Optional[str] = None,
        Name: Optional[str] = None,
        Description: Optional[str] = None,
        IsActive: Optional[bool] = None,
        ManufacturerID: Optional[int] = None,
        ManufacturerName: Optional[str] = None,
        ProductTypeID: Optional[int] = None,
        ProductTypeName: Optional[str] = None,
        PartNumber: Optional[str] = None,
        Attributes: Optional[list] = None,
        CreatedDate: Optional[str] = None,
        CreatedUid: Optional[str] = None,
        CreatedFullName: Optional[str] = None,
        ModifiedDate: Optional[str] = None,
        ModifiedUid: Optional[str] = None,
        ModifiedFullName: Optional[str] = None,
    ):
        self.ID = ID
        self.AppID = AppID
        self.AppName = AppName
        self.Name = Name
        self.Description = Description
        self.IsActive = IsActive
        self.ManufacturerID = ManufacturerID
        self.ManufacturerName = ManufacturerName
        self.ProductTypeID = ProductTypeID
        self.ProductTypeName = ProductTypeName
        self.PartNumber = PartNumber
        self.Attributes = Attributes
        self.CreatedDate = CreatedDate
        self.CreatedUid = CreatedUid
        self.CreatedFullName = CreatedFullName
        self.ModifiedDate = ModifiedDate
        self.ModifiedUid = ModifiedUid
        self.ModifiedFullName = ModifiedFullName
