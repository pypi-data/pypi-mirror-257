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

class AppointmentTemplateLine(_message.Message):
    __slots__ = ["id", "day", "hour_start", "hour_end", "order_numbers", "active", "external_id", "object_audit"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_START_FIELD_NUMBER: _ClassVar[int]
    HOUR_END_FIELD_NUMBER: _ClassVar[int]
    ORDER_NUMBERS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_AUDIT_FIELD_NUMBER: _ClassVar[int]
    id: str
    day: str
    hour_start: str
    hour_end: str
    order_numbers: int
    active: _wrappers_pb2.BoolValue
    external_id: str
    object_audit: _base_pb2.ObjectAudit
    def __init__(
        self,
        id: _Optional[str] = ...,
        day: _Optional[str] = ...,
        hour_start: _Optional[str] = ...,
        hour_end: _Optional[str] = ...,
        order_numbers: _Optional[int] = ...,
        active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        external_id: _Optional[str] = ...,
        object_audit: _Optional[_Union[_base_pb2.ObjectAudit, _Mapping]] = ...,
    ) -> None: ...

class AppointmentTemplateLineCreateRequest(_message.Message):
    __slots__ = ["day", "hour_start", "hour_end", "order_numbers", "external_id", "context"]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_START_FIELD_NUMBER: _ClassVar[int]
    HOUR_END_FIELD_NUMBER: _ClassVar[int]
    ORDER_NUMBERS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    day: str
    hour_start: str
    hour_end: str
    order_numbers: int
    external_id: str
    context: _base_pb2.Context
    def __init__(
        self,
        day: _Optional[str] = ...,
        hour_start: _Optional[str] = ...,
        hour_end: _Optional[str] = ...,
        order_numbers: _Optional[int] = ...,
        external_id: _Optional[str] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class AppointmentTemplateLineCreateResponse(_message.Message):
    __slots__ = ["appointment_template_line", "response_standard"]
    APPOINTMENT_TEMPLATE_LINE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    appointment_template_line: AppointmentTemplateLine
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        appointment_template_line: _Optional[_Union[AppointmentTemplateLine, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class AppointmentTemplateLineReadRequest(_message.Message):
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

class AppointmentTemplateLineReadResponse(_message.Message):
    __slots__ = ["appointment_template_lines", "meta_data", "response_standard"]
    APPOINTMENT_TEMPLATE_LINES_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    appointment_template_lines: _containers.RepeatedCompositeFieldContainer[AppointmentTemplateLine]
    meta_data: _base_pb2.MetaData
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        appointment_template_lines: _Optional[_Iterable[_Union[AppointmentTemplateLine, _Mapping]]] = ...,
        meta_data: _Optional[_Union[_base_pb2.MetaData, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class AppointmentTemplateLineUpdateRequest(_message.Message):
    __slots__ = ["appointment_template_line", "context"]
    APPOINTMENT_TEMPLATE_LINE_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    appointment_template_line: AppointmentTemplateLine
    context: _base_pb2.Context
    def __init__(
        self,
        appointment_template_line: _Optional[_Union[AppointmentTemplateLine, _Mapping]] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class AppointmentTemplateLineUpdateResponse(_message.Message):
    __slots__ = ["appointment_template_line", "response_standard"]
    APPOINTMENT_TEMPLATE_LINE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    appointment_template_line: AppointmentTemplateLine
    response_standard: _base_pb2.ResponseStandard
    def __init__(
        self,
        appointment_template_line: _Optional[_Union[AppointmentTemplateLine, _Mapping]] = ...,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
    ) -> None: ...

class AppointmentTemplateLineDeleteRequest(_message.Message):
    __slots__ = ["id", "context"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: str
    context: _base_pb2.Context
    def __init__(
        self, id: _Optional[str] = ..., context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...
    ) -> None: ...

class AppointmentTemplateLineDeleteResponse(_message.Message):
    __slots__ = ["response_standard"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    def __init__(self, response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...) -> None: ...
