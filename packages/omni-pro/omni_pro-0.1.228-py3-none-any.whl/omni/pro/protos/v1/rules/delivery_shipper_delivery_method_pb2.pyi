from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from omni.pro.protos.common import base_pb2 as _base_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class DeliveryShipperDeliveryMethod(_message.Message):
    __slots__ = ["id", "delivery_shipper_id", "delivery_method_id", "active", "external_id", "object_audit"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_SHIPPER_ID_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_METHOD_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_AUDIT_FIELD_NUMBER: _ClassVar[int]
    id: int
    delivery_shipper_id: int
    delivery_method_id: int
    active: bool
    external_id: str
    object_audit: _base_pb2.ObjectAudit
    def __init__(
        self,
        id: _Optional[int] = ...,
        delivery_shipper_id: _Optional[int] = ...,
        delivery_method_id: _Optional[int] = ...,
        active: bool = ...,
        external_id: _Optional[str] = ...,
        object_audit: _Optional[_Union[_base_pb2.ObjectAudit, _Mapping]] = ...,
    ) -> None: ...

class DeliveryShipperDeliveryMethodCreateRequest(_message.Message):
    __slots__ = ["delivery_shipper_id", "delivery_method_id", "external_id", "context"]
    DELIVERY_SHIPPER_ID_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_METHOD_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    delivery_shipper_id: int
    delivery_method_id: int
    external_id: str
    context: _base_pb2.Context
    def __init__(
        self,
        delivery_shipper_id: _Optional[int] = ...,
        delivery_method_id: _Optional[int] = ...,
        external_id: _Optional[str] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class DeliveryShipperDeliveryMethodCreateResponse(_message.Message):
    __slots__ = ["delivery_shipper_delivery_method", "response_standard"]
    DELIVERY_SHIPPER_DELIVERY_METHOD_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    delivery_shipper_delivery_method: DeliveryShipperDeliveryMethod
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        delivery_shipper_delivery_method: _Optional[_Union[DeliveryShipperDeliveryMethod, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class DeliveryShipperDeliveryMethodReadRequest(_message.Message):
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

class DeliveryShipperDeliveryMethodReadResponse(_message.Message):
    __slots__ = ["delivery_shipper_delivery_method", "meta_data", "response_standard"]
    DELIVERY_SHIPPER_DELIVERY_METHOD_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    delivery_shipper_delivery_method: _containers.RepeatedCompositeFieldContainer[DeliveryShipperDeliveryMethod]
    meta_data: _base_pb2.MetaData
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        delivery_shipper_delivery_method: _Optional[_Iterable[_Union[DeliveryShipperDeliveryMethod, _Mapping]]] = ...,
        meta_data: _Optional[_Union[_base_pb2.MetaData, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class DeliveryShipperDeliveryMethodUpdateRequest(_message.Message):
    __slots__ = ["delivery_shipper_delivery_method", "context"]
    DELIVERY_SHIPPER_DELIVERY_METHOD_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    delivery_shipper_delivery_method: DeliveryShipperDeliveryMethod
    context: _base_pb2.Context
    def __init__(
        self,
        delivery_shipper_delivery_method: _Optional[_Union[DeliveryShipperDeliveryMethod, _Mapping]] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class DeliveryShipperDeliveryMethodUpdateResponse(_message.Message):
    __slots__ = ["delivery_shipper_delivery_method", "response_standard"]
    DELIVERY_SHIPPER_DELIVERY_METHOD_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    delivery_shipper_delivery_method: DeliveryShipperDeliveryMethod
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        delivery_shipper_delivery_method: _Optional[_Union[DeliveryShipperDeliveryMethod, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class DeliveryShipperDeliveryMethodDeleteRequest(_message.Message):
    __slots__ = ["id", "context"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: int
    context: _base_pb2.Context
    def __init__(
        self, id: _Optional[int] = ..., context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...
    ) -> None: ...

class DeliveryShipperDeliveryMethodDeleteResponse(_message.Message):
    __slots__ = ["response_standard"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    def __init__(self, response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...) -> None: ...
