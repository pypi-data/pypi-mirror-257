from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from omni.pro.protos.common import base_pb2 as _base_pb2
from omni.pro.protos.v1.stock import location_pb2 as _location_pb2
from omni.pro.protos.v1.stock import product_pb2 as _product_pb2
from omni.pro.protos.v1.stock import uom_pb2 as _uom_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class Quant(_message.Message):
    __slots__ = [
        "id",
        "product",
        "location",
        "lote",
        "available_quantity",
        "reserved_quantity",
        "quantity",
        "uom",
        "active",
        "external_id",
        "object_audit",
    ]
    ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    LOTE_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    RESERVED_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    UOM_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_AUDIT_FIELD_NUMBER: _ClassVar[int]
    id: int
    product: _product_pb2.Product
    location: _location_pb2.Location
    lote: str
    available_quantity: float
    reserved_quantity: float
    quantity: float
    uom: _uom_pb2.Uom
    active: _wrappers_pb2.BoolValue
    external_id: str
    object_audit: _base_pb2.ObjectAudit
    def __init__(
        self,
        id: _Optional[int] = ...,
        product: _Optional[_Union[_product_pb2.Product, _Mapping]] = ...,
        location: _Optional[_Union[_location_pb2.Location, _Mapping]] = ...,
        lote: _Optional[str] = ...,
        available_quantity: _Optional[float] = ...,
        reserved_quantity: _Optional[float] = ...,
        quantity: _Optional[float] = ...,
        uom: _Optional[_Union[_uom_pb2.Uom, _Mapping]] = ...,
        active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        external_id: _Optional[str] = ...,
        object_audit: _Optional[_Union[_base_pb2.ObjectAudit, _Mapping]] = ...,
    ) -> None: ...

class QuantCreateRequest(_message.Message):
    __slots__ = [
        "product_id",
        "location_id",
        "lote",
        "available_quantity",
        "reserved_quantity",
        "quantity",
        "uom_id",
        "external_id",
        "context",
    ]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    LOTE_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    RESERVED_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    UOM_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    product_id: str
    location_id: int
    lote: str
    available_quantity: float
    reserved_quantity: float
    quantity: float
    uom_id: str
    external_id: str
    context: _base_pb2.Context
    def __init__(
        self,
        product_id: _Optional[str] = ...,
        location_id: _Optional[int] = ...,
        lote: _Optional[str] = ...,
        available_quantity: _Optional[float] = ...,
        reserved_quantity: _Optional[float] = ...,
        quantity: _Optional[float] = ...,
        uom_id: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class QuantCreateResponse(_message.Message):
    __slots__ = ["response_standard", "quant"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    QUANT_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    quant: Quant
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        quant: _Optional[_Union[Quant, _Mapping]] = ...,
    ) -> None: ...

class QuantReadRequest(_message.Message):
    __slots__ = ["group_by", "sort_by", "fields", "filter", "paginated", "id", "context"]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    SORT_BY_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGINATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    group_by: _containers.RepeatedCompositeFieldContainer[_base_pb2.GroupBy]
    sort_by: _base_pb2.SortBy
    fields: _base_pb2.Fields
    filter: _base_pb2.Filter
    paginated: _base_pb2.Paginated
    id: int
    context: _base_pb2.Context
    def __init__(
        self,
        group_by: _Optional[_Iterable[_Union[_base_pb2.GroupBy, _Mapping]]] = ...,
        sort_by: _Optional[_Union[_base_pb2.SortBy, _Mapping]] = ...,
        fields: _Optional[_Union[_base_pb2.Fields, _Mapping]] = ...,
        filter: _Optional[_Union[_base_pb2.Filter, _Mapping]] = ...,
        paginated: _Optional[_Union[_base_pb2.Paginated, _Mapping]] = ...,
        id: _Optional[int] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class QuantReadResponse(_message.Message):
    __slots__ = ["response_standard", "meta_data", "quants"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    QUANTS_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    meta_data: _base_pb2.MetaData
    quants: _containers.RepeatedCompositeFieldContainer[Quant]
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        meta_data: _Optional[_Union[_base_pb2.MetaData, _Mapping]] = ...,
        quants: _Optional[_Iterable[_Union[Quant, _Mapping]]] = ...,
    ) -> None: ...

class QuantUpdateRequest(_message.Message):
    __slots__ = ["quant", "context"]
    QUANT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    quant: Quant
    context: _base_pb2.Context
    def __init__(
        self,
        quant: _Optional[_Union[Quant, _Mapping]] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class QuantUpdateResponse(_message.Message):
    __slots__ = ["response_standard", "quant"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    QUANT_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    quant: Quant
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        quant: _Optional[_Union[Quant, _Mapping]] = ...,
    ) -> None: ...

class QuantDeleteRequest(_message.Message):
    __slots__ = ["id", "context"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: int
    context: _base_pb2.Context
    def __init__(
        self, id: _Optional[int] = ..., context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...
    ) -> None: ...

class QuantDeleteResponse(_message.Message):
    __slots__ = ["response_standard"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    def __init__(self, response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...) -> None: ...

class ProductAvailable(_message.Message):
    __slots__ = ["available", "available_quantity", "quant"]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    QUANT_FIELD_NUMBER: _ClassVar[int]
    available: _wrappers_pb2.BoolValue
    available_quantity: float
    quant: Quant
    def __init__(
        self,
        available: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        available_quantity: _Optional[float] = ...,
        quant: _Optional[_Union[Quant, _Mapping]] = ...,
    ) -> None: ...

class ProductAvailableRequest(_message.Message):
    __slots__ = ["location_id", "product_id", "product_sku", "required_quantity", "context"]
    LOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_SKU_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    location_id: int
    product_id: str
    product_sku: str
    required_quantity: float
    context: _base_pb2.Context
    def __init__(
        self,
        location_id: _Optional[int] = ...,
        product_id: _Optional[str] = ...,
        product_sku: _Optional[str] = ...,
        required_quantity: _Optional[float] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class ProductAvailableResponse(_message.Message):
    __slots__ = ["response_standard", "product_available"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    product_available: ProductAvailable
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        product_available: _Optional[_Union[ProductAvailable, _Mapping]] = ...,
    ) -> None: ...
