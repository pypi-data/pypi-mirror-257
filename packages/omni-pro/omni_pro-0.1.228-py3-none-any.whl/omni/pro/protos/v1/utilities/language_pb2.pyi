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

class Language(_message.Message):
    __slots__ = [
        "id",
        "name",
        "code",
        "code_iso",
        "direction",
        "date_format",
        "time_format",
        "decimal_point",
        "thousands_separator",
        "grouping",
        "week_start",
        "icon",
        "active",
        "external_id",
        "object_audit",
    ]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    CODE_ISO_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DATE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    TIME_FORMAT_FIELD_NUMBER: _ClassVar[int]
    DECIMAL_POINT_FIELD_NUMBER: _ClassVar[int]
    THOUSANDS_SEPARATOR_FIELD_NUMBER: _ClassVar[int]
    GROUPING_FIELD_NUMBER: _ClassVar[int]
    WEEK_START_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_AUDIT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    code: str
    code_iso: str
    direction: str
    date_format: str
    time_format: str
    decimal_point: str
    thousands_separator: str
    grouping: str
    week_start: str
    icon: bytes
    active: _wrappers_pb2.BoolValue
    external_id: str
    object_audit: _base_pb2.ObjectAudit
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        code: _Optional[str] = ...,
        code_iso: _Optional[str] = ...,
        direction: _Optional[str] = ...,
        date_format: _Optional[str] = ...,
        time_format: _Optional[str] = ...,
        decimal_point: _Optional[str] = ...,
        thousands_separator: _Optional[str] = ...,
        grouping: _Optional[str] = ...,
        week_start: _Optional[str] = ...,
        icon: _Optional[bytes] = ...,
        active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        external_id: _Optional[str] = ...,
        object_audit: _Optional[_Union[_base_pb2.ObjectAudit, _Mapping]] = ...,
    ) -> None: ...

class LanguageAddRequest(_message.Message):
    __slots__ = [
        "name",
        "code",
        "code_iso",
        "direction",
        "date_format",
        "time_format",
        "decimal_point",
        "thousands_separator",
        "grouping",
        "week_start",
        "icon",
        "active",
        "external_id",
        "context",
    ]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    CODE_ISO_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DATE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    TIME_FORMAT_FIELD_NUMBER: _ClassVar[int]
    DECIMAL_POINT_FIELD_NUMBER: _ClassVar[int]
    THOUSANDS_SEPARATOR_FIELD_NUMBER: _ClassVar[int]
    GROUPING_FIELD_NUMBER: _ClassVar[int]
    WEEK_START_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    name: str
    code: str
    code_iso: str
    direction: str
    date_format: str
    time_format: str
    decimal_point: str
    thousands_separator: str
    grouping: str
    week_start: str
    icon: bytes
    active: _wrappers_pb2.BoolValue
    external_id: str
    context: _base_pb2.Context
    def __init__(
        self,
        name: _Optional[str] = ...,
        code: _Optional[str] = ...,
        code_iso: _Optional[str] = ...,
        direction: _Optional[str] = ...,
        date_format: _Optional[str] = ...,
        time_format: _Optional[str] = ...,
        decimal_point: _Optional[str] = ...,
        thousands_separator: _Optional[str] = ...,
        grouping: _Optional[str] = ...,
        week_start: _Optional[str] = ...,
        icon: _Optional[bytes] = ...,
        active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        external_id: _Optional[str] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class LanguageAddResponse(_message.Message):
    __slots__ = ["response_standard", "language"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    language: Language
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        language: _Optional[_Union[Language, _Mapping]] = ...,
    ) -> None: ...

class LanguageReadRequest(_message.Message):
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

class LanguageReadResponse(_message.Message):
    __slots__ = ["response_standard", "meta_data", "languages"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    LANGUAGES_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    meta_data: _base_pb2.MetaData
    languages: _containers.RepeatedCompositeFieldContainer[Language]
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        meta_data: _Optional[_Union[_base_pb2.MetaData, _Mapping]] = ...,
        languages: _Optional[_Iterable[_Union[Language, _Mapping]]] = ...,
    ) -> None: ...

class LanguageUpdateRequest(_message.Message):
    __slots__ = ["language", "context"]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    language: Language
    context: _base_pb2.Context
    def __init__(
        self,
        language: _Optional[_Union[Language, _Mapping]] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class LanguageUpdateResponse(_message.Message):
    __slots__ = ["response_standard", "language"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    language: Language
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        language: _Optional[_Union[Language, _Mapping]] = ...,
    ) -> None: ...

class LanguageDeleteRequest(_message.Message):
    __slots__ = ["id", "context"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: str
    context: _base_pb2.Context
    def __init__(
        self, id: _Optional[str] = ..., context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...
    ) -> None: ...

class LanguageDeleteResponse(_message.Message):
    __slots__ = ["response_standard"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    def __init__(self, response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...) -> None: ...
