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
from omni.pro.protos.v1.rules import location_pb2 as _location_pb2
from omni.pro.protos.v1.rules import warehouse_pb2 as _warehouse_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class WarehouseHierarchy(_message.Message):
    __slots__ = [
        "id",
        "name",
        "code",
        "warehouse",
        "location",
        "quantity_security",
        "sequence",
        "sequence_order",
        "gift_code",
        "active",
        "external_id",
        "object_audit",
    ]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_SECURITY_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_ORDER_FIELD_NUMBER: _ClassVar[int]
    GIFT_CODE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_AUDIT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    code: str
    warehouse: _warehouse_pb2.Warehouse
    location: _location_pb2.Location
    quantity_security: float
    sequence: int
    sequence_order: _wrappers_pb2.BoolValue
    gift_code: str
    active: _wrappers_pb2.BoolValue
    external_id: str
    object_audit: _base_pb2.ObjectAudit
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        code: _Optional[str] = ...,
        warehouse: _Optional[_Union[_warehouse_pb2.Warehouse, _Mapping]] = ...,
        location: _Optional[_Union[_location_pb2.Location, _Mapping]] = ...,
        quantity_security: _Optional[float] = ...,
        sequence: _Optional[int] = ...,
        sequence_order: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        gift_code: _Optional[str] = ...,
        active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        external_id: _Optional[str] = ...,
        object_audit: _Optional[_Union[_base_pb2.ObjectAudit, _Mapping]] = ...,
    ) -> None: ...

class WarehouseHierarchyCreateRequest(_message.Message):
    __slots__ = [
        "name",
        "code",
        "warehouse_id",
        "location_id",
        "quantity_security",
        "sequence",
        "gift_code",
        "sequence_order",
        "external_id",
        "context",
    ]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_SECURITY_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    GIFT_CODE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_ORDER_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    name: str
    code: str
    warehouse_id: int
    location_id: int
    quantity_security: float
    sequence: int
    gift_code: str
    sequence_order: _wrappers_pb2.BoolValue
    external_id: str
    context: _base_pb2.Context
    def __init__(
        self,
        name: _Optional[str] = ...,
        code: _Optional[str] = ...,
        warehouse_id: _Optional[int] = ...,
        location_id: _Optional[int] = ...,
        quantity_security: _Optional[float] = ...,
        sequence: _Optional[int] = ...,
        gift_code: _Optional[str] = ...,
        sequence_order: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        external_id: _Optional[str] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class WarehouseHierarchyCreateResponse(_message.Message):
    __slots__ = ["warehouse_hierarchy", "response_standard"]
    WAREHOUSE_HIERARCHY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    warehouse_hierarchy: WarehouseHierarchy
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        warehouse_hierarchy: _Optional[_Union[WarehouseHierarchy, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class WarehouseHierarchyReadRequest(_message.Message):
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

class WarehouseHierarchyReadResponse(_message.Message):
    __slots__ = ["warehouses_hierarchy", "meta_data", "response_standard"]
    WAREHOUSES_HIERARCHY_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    warehouses_hierarchy: _containers.RepeatedCompositeFieldContainer[WarehouseHierarchy]
    meta_data: _base_pb2.MetaData
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        warehouses_hierarchy: _Optional[_Iterable[_Union[WarehouseHierarchy, _Mapping]]] = ...,
        meta_data: _Optional[_Union[_base_pb2.MetaData, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class WarehouseHierarchyUpdateRequest(_message.Message):
    __slots__ = ["warehouse_hierarchy", "context"]
    WAREHOUSE_HIERARCHY_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    warehouse_hierarchy: WarehouseHierarchy
    context: _base_pb2.Context
    def __init__(
        self,
        warehouse_hierarchy: _Optional[_Union[WarehouseHierarchy, _Mapping]] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class WarehouseHierarchyUpdateResponse(_message.Message):
    __slots__ = ["warehouse_hierarchy", "response_standard"]
    WAREHOUSE_HIERARCHY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    warehouse_hierarchy: WarehouseHierarchy
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        warehouse_hierarchy: _Optional[_Union[WarehouseHierarchy, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class WarehouseHierarchyDeleteRequest(_message.Message):
    __slots__ = ["id", "context"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: str
    context: _base_pb2.Context
    def __init__(
        self, id: _Optional[str] = ..., context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...
    ) -> None: ...

class WarehouseHierarchyDeleteResponse(_message.Message):
    __slots__ = ["response_standard"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    def __init__(self, response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...) -> None: ...
