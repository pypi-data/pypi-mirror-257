from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from omni.pro.protos.common import base_pb2 as _base_pb2
from omni.pro.protos.v1.rules import delivery_locality_pb2 as _delivery_locality_pb2
from omni.pro.protos.v1.rules import delivery_schedule_pb2 as _delivery_schedule_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class Warehouse(_message.Message):
    __slots__ = [
        "id",
        "name",
        "code",
        "warehouse_sql_id",
        "locality_available",
        "loc_stock_sql_id",
        "external_id",
        "schedule_template",
        "object_audit",
    ]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_SQL_ID_FIELD_NUMBER: _ClassVar[int]
    LOCALITY_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    LOC_STOCK_SQL_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_AUDIT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    code: str
    warehouse_sql_id: int
    locality_available: _delivery_locality_pb2.DeliveryLocality
    loc_stock_sql_id: int
    external_id: str
    schedule_template: _delivery_schedule_pb2.DeliverySchedule
    object_audit: _base_pb2.ObjectAudit
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        code: _Optional[str] = ...,
        warehouse_sql_id: _Optional[int] = ...,
        locality_available: _Optional[_Union[_delivery_locality_pb2.DeliveryLocality, _Mapping]] = ...,
        loc_stock_sql_id: _Optional[int] = ...,
        external_id: _Optional[str] = ...,
        schedule_template: _Optional[_Union[_delivery_schedule_pb2.DeliverySchedule, _Mapping]] = ...,
        object_audit: _Optional[_Union[_base_pb2.ObjectAudit, _Mapping]] = ...,
    ) -> None: ...

class WarehouseCreateRequest(_message.Message):
    __slots__ = [
        "name",
        "code",
        "warehouse_sql_id",
        "locality_available_id",
        "loc_stock_sql_id",
        "external_id",
        "schedule_template_id",
        "context",
    ]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_SQL_ID_FIELD_NUMBER: _ClassVar[int]
    LOCALITY_AVAILABLE_ID_FIELD_NUMBER: _ClassVar[int]
    LOC_STOCK_SQL_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    name: str
    code: str
    warehouse_sql_id: int
    locality_available_id: str
    loc_stock_sql_id: int
    external_id: str
    schedule_template_id: str
    context: _base_pb2.Context
    def __init__(
        self,
        name: _Optional[str] = ...,
        code: _Optional[str] = ...,
        warehouse_sql_id: _Optional[int] = ...,
        locality_available_id: _Optional[str] = ...,
        loc_stock_sql_id: _Optional[int] = ...,
        external_id: _Optional[str] = ...,
        schedule_template_id: _Optional[str] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class WarehouseCreateResponse(_message.Message):
    __slots__ = ["warehouse", "response_standard"]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    warehouse: Warehouse
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        warehouse: _Optional[_Union[Warehouse, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class WarehouseReadRequest(_message.Message):
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

class WarehouseReadResponse(_message.Message):
    __slots__ = ["warehouses", "meta_data", "response_standard"]
    WAREHOUSES_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    warehouses: _containers.RepeatedCompositeFieldContainer[Warehouse]
    meta_data: _base_pb2.MetaData
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        warehouses: _Optional[_Iterable[_Union[Warehouse, _Mapping]]] = ...,
        meta_data: _Optional[_Union[_base_pb2.MetaData, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class WarehouseUpdateRequest(_message.Message):
    __slots__ = ["warehouse", "context"]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    warehouse: Warehouse
    context: _base_pb2.Context
    def __init__(
        self,
        warehouse: _Optional[_Union[Warehouse, _Mapping]] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class WarehouseUpdateResponse(_message.Message):
    __slots__ = ["warehouse", "response_standard"]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    warehouse: Warehouse
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        warehouse: _Optional[_Union[Warehouse, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class WarehouseDeleteRequest(_message.Message):
    __slots__ = ["id", "warehouse_sql_id", "context"]
    ID_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_SQL_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: str
    warehouse_sql_id: int
    context: _base_pb2.Context
    def __init__(
        self,
        id: _Optional[str] = ...,
        warehouse_sql_id: _Optional[int] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class WarehouseDeleteResponse(_message.Message):
    __slots__ = ["response_standard"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    def __init__(self, response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...) -> None: ...
