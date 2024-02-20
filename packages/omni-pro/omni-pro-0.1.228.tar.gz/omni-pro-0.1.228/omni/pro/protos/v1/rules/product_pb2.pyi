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

DESCRIPTOR: _descriptor.FileDescriptor

class Product(_message.Message):
    __slots__ = [
        "id",
        "name",
        "sku",
        "category_code",
        "weight_value",
        "weight_uom_code",
        "height_value",
        "height_uom_code",
        "width_value",
        "width_uom_code",
        "length_value",
        "length_uom_code",
        "volume_value",
        "volume_uom_code",
        "active",
        "product_doc_id",
        "external_id",
        "special_conditions",
        "object_audit",
    ]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SKU_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_CODE_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_VALUE_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_UOM_CODE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_VALUE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_UOM_CODE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_VALUE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_UOM_CODE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_VALUE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_UOM_CODE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_VALUE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_UOM_CODE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_DOC_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    OBJECT_AUDIT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    sku: str
    category_code: str
    weight_value: float
    weight_uom_code: str
    height_value: float
    height_uom_code: str
    width_value: float
    width_uom_code: str
    length_value: float
    length_uom_code: str
    volume_value: float
    volume_uom_code: str
    active: _wrappers_pb2.BoolValue
    product_doc_id: str
    external_id: str
    special_conditions: _containers.RepeatedScalarFieldContainer[str]
    object_audit: _base_pb2.ObjectAudit
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        sku: _Optional[str] = ...,
        category_code: _Optional[str] = ...,
        weight_value: _Optional[float] = ...,
        weight_uom_code: _Optional[str] = ...,
        height_value: _Optional[float] = ...,
        height_uom_code: _Optional[str] = ...,
        width_value: _Optional[float] = ...,
        width_uom_code: _Optional[str] = ...,
        length_value: _Optional[float] = ...,
        length_uom_code: _Optional[str] = ...,
        volume_value: _Optional[float] = ...,
        volume_uom_code: _Optional[str] = ...,
        active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        product_doc_id: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        special_conditions: _Optional[_Iterable[str]] = ...,
        object_audit: _Optional[_Union[_base_pb2.ObjectAudit, _Mapping]] = ...,
    ) -> None: ...

class ProductCreateRequest(_message.Message):
    __slots__ = [
        "name",
        "sku",
        "category_code",
        "weight_value",
        "weight_uom_code",
        "height_value",
        "height_uom_code",
        "width_value",
        "width_uom_code",
        "length_value",
        "length_uom_code",
        "volume_value",
        "volume_uom_code",
        "product_doc_id",
        "external_id",
        "special_conditions",
        "context",
    ]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SKU_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_CODE_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_VALUE_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_UOM_CODE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_VALUE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_UOM_CODE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_VALUE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_UOM_CODE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_VALUE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_UOM_CODE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_VALUE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_UOM_CODE_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_DOC_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    name: str
    sku: str
    category_code: str
    weight_value: float
    weight_uom_code: str
    height_value: float
    height_uom_code: str
    width_value: float
    width_uom_code: str
    length_value: float
    length_uom_code: str
    volume_value: float
    volume_uom_code: str
    product_doc_id: str
    external_id: str
    special_conditions: _containers.RepeatedScalarFieldContainer[str]
    context: _base_pb2.Context
    def __init__(
        self,
        name: _Optional[str] = ...,
        sku: _Optional[str] = ...,
        category_code: _Optional[str] = ...,
        weight_value: _Optional[float] = ...,
        weight_uom_code: _Optional[str] = ...,
        height_value: _Optional[float] = ...,
        height_uom_code: _Optional[str] = ...,
        width_value: _Optional[float] = ...,
        width_uom_code: _Optional[str] = ...,
        length_value: _Optional[float] = ...,
        length_uom_code: _Optional[str] = ...,
        volume_value: _Optional[float] = ...,
        volume_uom_code: _Optional[str] = ...,
        product_doc_id: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        special_conditions: _Optional[_Iterable[str]] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class ProductCreateResponse(_message.Message):
    __slots__ = ["product", "response_standard"]
    PRODUCT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    product: Product
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        product: _Optional[_Union[Product, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class ProductReadRequest(_message.Message):
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
    id: str
    context: _base_pb2.Context
    def __init__(
        self,
        group_by: _Optional[_Iterable[_Union[_base_pb2.GroupBy, _Mapping]]] = ...,
        sort_by: _Optional[_Union[_base_pb2.SortBy, _Mapping]] = ...,
        fields: _Optional[_Union[_base_pb2.Fields, _Mapping]] = ...,
        filter: _Optional[_Union[_base_pb2.Filter, _Mapping]] = ...,
        paginated: _Optional[_Union[_base_pb2.Paginated, _Mapping]] = ...,
        id: _Optional[str] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class ProductReadResponse(_message.Message):
    __slots__ = ["products", "meta_data", "response_standard"]
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    products: _containers.RepeatedCompositeFieldContainer[Product]
    meta_data: _base_pb2.MetaData
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        products: _Optional[_Iterable[_Union[Product, _Mapping]]] = ...,
        meta_data: _Optional[_Union[_base_pb2.MetaData, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class ProductUpdateRequest(_message.Message):
    __slots__ = ["product", "context"]
    PRODUCT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    product: Product
    context: _base_pb2.Context
    def __init__(
        self,
        product: _Optional[_Union[Product, _Mapping]] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class ProductUpdateResponse(_message.Message):
    __slots__ = ["product", "response_standard"]
    PRODUCT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    product: Product
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        product: _Optional[_Union[Product, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class ProductDeleteRequest(_message.Message):
    __slots__ = ["product_doc_id", "context"]
    PRODUCT_DOC_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    product_doc_id: str
    context: _base_pb2.Context
    def __init__(
        self, product_doc_id: _Optional[str] = ..., context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...
    ) -> None: ...

class ProductDeleteResponse(_message.Message):
    __slots__ = ["response_standard"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    def __init__(self, response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...) -> None: ...
