from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from omni.pro.protos.common import base_pb2 as _base_pb2
from omni.pro.protos.v1.stock import country_pb2 as _country_pb2
from omni.pro.protos.v1.stock import location_pb2 as _location_pb2
from omni.pro.protos.v1.stock import picking_type_pb2 as _picking_type_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class Warehouse(_message.Message):
    __slots__ = [
        "id",
        "name",
        "code",
        "country",
        "country_code",
        "territory_matrix_value",
        "address",
        "complement",
        "active",
        "delivery_steps",
        "reception_steps",
        "locality_available",
        "view_location",
        "loc_stock",
        "wh_input_stock_loc",
        "wh_qc_stock_loc",
        "wh_pack_stock_loc",
        "wh_output_stock_loc",
        "in_type",
        "int_type",
        "pick_type",
        "pack_type",
        "out_type",
        "external_id",
        "locality_available_rule",
        "schedule_template_rule",
        "ecommerce_code",
        "object_audit",
    ]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    TERRITORY_MATRIX_VALUE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COMPLEMENT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_STEPS_FIELD_NUMBER: _ClassVar[int]
    RECEPTION_STEPS_FIELD_NUMBER: _ClassVar[int]
    LOCALITY_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    VIEW_LOCATION_FIELD_NUMBER: _ClassVar[int]
    LOC_STOCK_FIELD_NUMBER: _ClassVar[int]
    WH_INPUT_STOCK_LOC_FIELD_NUMBER: _ClassVar[int]
    WH_QC_STOCK_LOC_FIELD_NUMBER: _ClassVar[int]
    WH_PACK_STOCK_LOC_FIELD_NUMBER: _ClassVar[int]
    WH_OUTPUT_STOCK_LOC_FIELD_NUMBER: _ClassVar[int]
    IN_TYPE_FIELD_NUMBER: _ClassVar[int]
    INT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PICK_TYPE_FIELD_NUMBER: _ClassVar[int]
    PACK_TYPE_FIELD_NUMBER: _ClassVar[int]
    OUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    LOCALITY_AVAILABLE_RULE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_TEMPLATE_RULE_FIELD_NUMBER: _ClassVar[int]
    ECOMMERCE_CODE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_AUDIT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    code: str
    country: _country_pb2.Country
    country_code: str
    territory_matrix_value: _struct_pb2.ListValue
    address: str
    complement: str
    active: _wrappers_pb2.BoolValue
    delivery_steps: str
    reception_steps: str
    locality_available: _wrappers_pb2.StringValue
    view_location: _location_pb2.Location
    loc_stock: _location_pb2.Location
    wh_input_stock_loc: _location_pb2.Location
    wh_qc_stock_loc: _location_pb2.Location
    wh_pack_stock_loc: _location_pb2.Location
    wh_output_stock_loc: _location_pb2.Location
    in_type: _picking_type_pb2.PickingType
    int_type: _picking_type_pb2.PickingType
    pick_type: _picking_type_pb2.PickingType
    pack_type: _picking_type_pb2.PickingType
    out_type: _picking_type_pb2.PickingType
    external_id: str
    locality_available_rule: str
    schedule_template_rule: str
    ecommerce_code: str
    object_audit: _base_pb2.ObjectAudit
    def __init__(
        self,
        id: _Optional[int] = ...,
        name: _Optional[str] = ...,
        code: _Optional[str] = ...,
        country: _Optional[_Union[_country_pb2.Country, _Mapping]] = ...,
        country_code: _Optional[str] = ...,
        territory_matrix_value: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ...,
        address: _Optional[str] = ...,
        complement: _Optional[str] = ...,
        active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        delivery_steps: _Optional[str] = ...,
        reception_steps: _Optional[str] = ...,
        locality_available: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...,
        view_location: _Optional[_Union[_location_pb2.Location, _Mapping]] = ...,
        loc_stock: _Optional[_Union[_location_pb2.Location, _Mapping]] = ...,
        wh_input_stock_loc: _Optional[_Union[_location_pb2.Location, _Mapping]] = ...,
        wh_qc_stock_loc: _Optional[_Union[_location_pb2.Location, _Mapping]] = ...,
        wh_pack_stock_loc: _Optional[_Union[_location_pb2.Location, _Mapping]] = ...,
        wh_output_stock_loc: _Optional[_Union[_location_pb2.Location, _Mapping]] = ...,
        in_type: _Optional[_Union[_picking_type_pb2.PickingType, _Mapping]] = ...,
        int_type: _Optional[_Union[_picking_type_pb2.PickingType, _Mapping]] = ...,
        pick_type: _Optional[_Union[_picking_type_pb2.PickingType, _Mapping]] = ...,
        pack_type: _Optional[_Union[_picking_type_pb2.PickingType, _Mapping]] = ...,
        out_type: _Optional[_Union[_picking_type_pb2.PickingType, _Mapping]] = ...,
        external_id: _Optional[str] = ...,
        locality_available_rule: _Optional[str] = ...,
        schedule_template_rule: _Optional[str] = ...,
        ecommerce_code: _Optional[str] = ...,
        object_audit: _Optional[_Union[_base_pb2.ObjectAudit, _Mapping]] = ...,
    ) -> None: ...

class WarehouseCreateRequest(_message.Message):
    __slots__ = [
        "name",
        "code",
        "country_code",
        "territory_matrix_value",
        "address",
        "complement",
        "delivery_steps",
        "reception_steps",
        "locality_available",
        "external_id",
        "locality_available_id",
        "schedule_template_id",
        "ecommerce_code",
        "context",
    ]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    TERRITORY_MATRIX_VALUE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COMPLEMENT_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_STEPS_FIELD_NUMBER: _ClassVar[int]
    RECEPTION_STEPS_FIELD_NUMBER: _ClassVar[int]
    LOCALITY_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    LOCALITY_AVAILABLE_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    ECOMMERCE_CODE_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    name: str
    code: str
    country_code: str
    territory_matrix_value: _struct_pb2.ListValue
    address: str
    complement: str
    delivery_steps: str
    reception_steps: str
    locality_available: str
    external_id: str
    locality_available_id: str
    schedule_template_id: str
    ecommerce_code: str
    context: _base_pb2.Context
    def __init__(
        self,
        name: _Optional[str] = ...,
        code: _Optional[str] = ...,
        country_code: _Optional[str] = ...,
        territory_matrix_value: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ...,
        address: _Optional[str] = ...,
        complement: _Optional[str] = ...,
        delivery_steps: _Optional[str] = ...,
        reception_steps: _Optional[str] = ...,
        locality_available: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        locality_available_id: _Optional[str] = ...,
        schedule_template_id: _Optional[str] = ...,
        ecommerce_code: _Optional[str] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class WarehouseCreateResponse(_message.Message):
    __slots__ = ["response_standard", "warehouse"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    warehouse: Warehouse
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        warehouse: _Optional[_Union[Warehouse, _Mapping]] = ...,
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

class WarehouseReadResponse(_message.Message):
    __slots__ = ["response_standard", "meta_data", "warehouses"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSES_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    meta_data: _base_pb2.MetaData
    warehouses: _containers.RepeatedCompositeFieldContainer[Warehouse]
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        meta_data: _Optional[_Union[_base_pb2.MetaData, _Mapping]] = ...,
        warehouses: _Optional[_Iterable[_Union[Warehouse, _Mapping]]] = ...,
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
    __slots__ = ["response_standard", "warehouse"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    warehouse: Warehouse
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        warehouse: _Optional[_Union[Warehouse, _Mapping]] = ...,
    ) -> None: ...

class WarehouseDeleteRequest(_message.Message):
    __slots__ = ["id", "context"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: int
    context: _base_pb2.Context
    def __init__(
        self, id: _Optional[int] = ..., context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...
    ) -> None: ...

class WarehouseDeleteResponse(_message.Message):
    __slots__ = ["response_standard"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    def __init__(self, response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...) -> None: ...
