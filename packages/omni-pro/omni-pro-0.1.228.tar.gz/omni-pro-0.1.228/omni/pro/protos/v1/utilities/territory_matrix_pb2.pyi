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

DESCRIPTOR: _descriptor.FileDescriptor

class TerritoryMatrix(_message.Message):
    __slots__ = ["id", "sequence", "name", "code", "active", "country_id", "external_id", "object_audit"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_AUDIT_FIELD_NUMBER: _ClassVar[int]
    id: str
    sequence: int
    name: str
    code: str
    active: _wrappers_pb2.BoolValue
    country_id: str
    external_id: str
    object_audit: _base_pb2.ObjectAudit
    def __init__(
        self,
        id: _Optional[str] = ...,
        sequence: _Optional[int] = ...,
        name: _Optional[str] = ...,
        code: _Optional[str] = ...,
        active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        country_id: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        object_audit: _Optional[_Union[_base_pb2.ObjectAudit, _Mapping]] = ...,
    ) -> None: ...

class TerritoryMatrixAddRequest(_message.Message):
    __slots__ = ["country_id", "sequence", "name", "code", "active", "external_id", "context"]
    COUNTRY_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    country_id: str
    sequence: int
    name: str
    code: str
    active: _wrappers_pb2.BoolValue
    external_id: str
    context: _base_pb2.Context
    def __init__(
        self,
        country_id: _Optional[str] = ...,
        sequence: _Optional[int] = ...,
        name: _Optional[str] = ...,
        code: _Optional[str] = ...,
        active: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...,
        external_id: _Optional[str] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class TerritoryMatrixAddResponse(_message.Message):
    __slots__ = ["response_standard", "territory_matrixes"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    TERRITORY_MATRIXES_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    territory_matrixes: TerritoryMatrix
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        territory_matrixes: _Optional[_Union[TerritoryMatrix, _Mapping]] = ...,
    ) -> None: ...

class TerritoryMatrixReadRequest(_message.Message):
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

class TerritoryMatrixReadResponse(_message.Message):
    __slots__ = ["response_standard", "meta_data", "territory_matrixes"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    META_DATA_FIELD_NUMBER: _ClassVar[int]
    TERRITORY_MATRIXES_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    meta_data: _base_pb2.MetaData
    territory_matrixes: _containers.RepeatedCompositeFieldContainer[TerritoryMatrix]
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        meta_data: _Optional[_Union[_base_pb2.MetaData, _Mapping]] = ...,
        territory_matrixes: _Optional[_Iterable[_Union[TerritoryMatrix, _Mapping]]] = ...,
    ) -> None: ...

class TerritoryMatrixUpdateRequest(_message.Message):
    __slots__ = ["territory_matrix", "context"]
    TERRITORY_MATRIX_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    territory_matrix: TerritoryMatrix
    context: _base_pb2.Context
    def __init__(
        self,
        territory_matrix: _Optional[_Union[TerritoryMatrix, _Mapping]] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class TerritoryMatrixUpdateResponse(_message.Message):
    __slots__ = ["response_standard", "territory_matrixes"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    TERRITORY_MATRIXES_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    territory_matrixes: TerritoryMatrix
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        territory_matrixes: _Optional[_Union[TerritoryMatrix, _Mapping]] = ...,
    ) -> None: ...

class TerritoryMatrixDeleteRequest(_message.Message):
    __slots__ = ["id", "context"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: str
    context: _base_pb2.Context
    def __init__(
        self, id: _Optional[str] = ..., context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...
    ) -> None: ...

class TerritoryMatrixDeleteResponse(_message.Message):
    __slots__ = ["response_standard"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    def __init__(self, response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...) -> None: ...

class TerritoryMatrixLoadRequest(_message.Message):
    __slots__ = ["country_code", "csv_name", "context"]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    CSV_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    country_code: str
    csv_name: str
    context: _base_pb2.Context
    def __init__(
        self,
        country_code: _Optional[str] = ...,
        csv_name: _Optional[str] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class TerritoryMatrixLoadResponse(_message.Message):
    __slots__ = ["response_standard"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    def __init__(self, response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...) -> None: ...

class TerritoryMatrixStructureRequest(_message.Message):
    __slots__ = ["territorymatrix", "parent_code", "filter", "context"]
    TERRITORYMATRIX_FIELD_NUMBER: _ClassVar[int]
    PARENT_CODE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    territorymatrix: TerritoryMatrix
    parent_code: str
    filter: _struct_pb2.Struct
    context: _base_pb2.Context
    def __init__(
        self,
        territorymatrix: _Optional[_Union[TerritoryMatrix, _Mapping]] = ...,
        parent_code: _Optional[str] = ...,
        filter: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        context: _Optional[_Union[_base_pb2.Context, _Mapping]] = ...,
    ) -> None: ...

class TerritoryMatrixStructureResponse(_message.Message):
    __slots__ = ["response_standard", "territory_matrixes"]
    RESPONSE_STANDARD_FIELD_NUMBER: _ClassVar[int]
    TERRITORY_MATRIXES_FIELD_NUMBER: _ClassVar[int]
    response_standard: _base_pb2.ResponseStandard
    territory_matrixes: _struct_pb2.ListValue
    def __init__(
        self,
        response_standard: _Optional[_Union[_base_pb2.ResponseStandard, _Mapping]] = ...,
        territory_matrixes: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ...,
    ) -> None: ...
