from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AggregateRequest(_message.Message):
    __slots__ = ["aggregates", "collectionname", "hint", "queryas"]
    AGGREGATES_FIELD_NUMBER: _ClassVar[int]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    HINT_FIELD_NUMBER: _ClassVar[int]
    QUERYAS_FIELD_NUMBER: _ClassVar[int]
    aggregates: str
    collectionname: str
    hint: str
    queryas: str
    def __init__(self, collectionname: _Optional[str] = ..., aggregates: _Optional[str] = ..., queryas: _Optional[str] = ..., hint: _Optional[str] = ...) -> None: ...

class AggregateResponse(_message.Message):
    __slots__ = ["results"]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: str
    def __init__(self, results: _Optional[str] = ...) -> None: ...

class CountRequest(_message.Message):
    __slots__ = ["collectionname", "query", "queryas"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    QUERYAS_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    query: str
    queryas: str
    def __init__(self, collectionname: _Optional[str] = ..., query: _Optional[str] = ..., queryas: _Optional[str] = ...) -> None: ...

class CountResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: _Optional[int] = ...) -> None: ...

class DeleteManyRequest(_message.Message):
    __slots__ = ["collectionname", "ids", "query", "recursive"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    RECURSIVE_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    ids: _containers.RepeatedScalarFieldContainer[str]
    query: str
    recursive: bool
    def __init__(self, collectionname: _Optional[str] = ..., query: _Optional[str] = ..., recursive: bool = ..., ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteManyResponse(_message.Message):
    __slots__ = ["affectedrows"]
    AFFECTEDROWS_FIELD_NUMBER: _ClassVar[int]
    affectedrows: int
    def __init__(self, affectedrows: _Optional[int] = ...) -> None: ...

class DeleteOneRequest(_message.Message):
    __slots__ = ["collectionname", "id", "recursive"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RECURSIVE_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    id: str
    recursive: bool
    def __init__(self, collectionname: _Optional[str] = ..., id: _Optional[str] = ..., recursive: bool = ...) -> None: ...

class DeleteOneResponse(_message.Message):
    __slots__ = ["affectedrows"]
    AFFECTEDROWS_FIELD_NUMBER: _ClassVar[int]
    affectedrows: int
    def __init__(self, affectedrows: _Optional[int] = ...) -> None: ...

class DropCollectionRequest(_message.Message):
    __slots__ = ["collectionname"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    def __init__(self, collectionname: _Optional[str] = ...) -> None: ...

class DropCollectionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetDocumentVersionRequest(_message.Message):
    __slots__ = ["collectionname", "decrypt", "id", "version"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    DECRYPT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    decrypt: bool
    id: str
    version: int
    def __init__(self, collectionname: _Optional[str] = ..., id: _Optional[str] = ..., version: _Optional[int] = ..., decrypt: bool = ...) -> None: ...

class GetDocumentVersionResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class InsertManyRequest(_message.Message):
    __slots__ = ["collectionname", "items", "j", "skipresults", "w"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    J_FIELD_NUMBER: _ClassVar[int]
    SKIPRESULTS_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    items: str
    j: bool
    skipresults: bool
    w: int
    def __init__(self, collectionname: _Optional[str] = ..., items: _Optional[str] = ..., w: _Optional[int] = ..., j: bool = ..., skipresults: bool = ...) -> None: ...

class InsertManyResponse(_message.Message):
    __slots__ = ["results"]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: str
    def __init__(self, results: _Optional[str] = ...) -> None: ...

class InsertOneRequest(_message.Message):
    __slots__ = ["collectionname", "item", "j", "w"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    J_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    item: str
    j: bool
    w: int
    def __init__(self, collectionname: _Optional[str] = ..., item: _Optional[str] = ..., w: _Optional[int] = ..., j: bool = ...) -> None: ...

class InsertOneResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class InsertOrUpdateManyRequest(_message.Message):
    __slots__ = ["collectionname", "items", "j", "skipresults", "uniqeness", "w"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    J_FIELD_NUMBER: _ClassVar[int]
    SKIPRESULTS_FIELD_NUMBER: _ClassVar[int]
    UNIQENESS_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    items: str
    j: bool
    skipresults: bool
    uniqeness: str
    w: int
    def __init__(self, collectionname: _Optional[str] = ..., uniqeness: _Optional[str] = ..., items: _Optional[str] = ..., w: _Optional[int] = ..., j: bool = ..., skipresults: bool = ...) -> None: ...

class InsertOrUpdateManyResponse(_message.Message):
    __slots__ = ["results"]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: str
    def __init__(self, results: _Optional[str] = ...) -> None: ...

class InsertOrUpdateOneRequest(_message.Message):
    __slots__ = ["collectionname", "item", "j", "uniqeness", "w"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    J_FIELD_NUMBER: _ClassVar[int]
    UNIQENESS_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    item: str
    j: bool
    uniqeness: str
    w: int
    def __init__(self, collectionname: _Optional[str] = ..., uniqeness: _Optional[str] = ..., item: _Optional[str] = ..., w: _Optional[int] = ..., j: bool = ...) -> None: ...

class InsertOrUpdateOneResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class ListCollectionsRequest(_message.Message):
    __slots__ = ["includehist"]
    INCLUDEHIST_FIELD_NUMBER: _ClassVar[int]
    includehist: bool
    def __init__(self, includehist: bool = ...) -> None: ...

class ListCollectionsResponse(_message.Message):
    __slots__ = ["results"]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: str
    def __init__(self, results: _Optional[str] = ...) -> None: ...

class QueryRequest(_message.Message):
    __slots__ = ["collectionname", "orderby", "projection", "query", "queryas", "skip", "top"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    ORDERBY_FIELD_NUMBER: _ClassVar[int]
    PROJECTION_FIELD_NUMBER: _ClassVar[int]
    QUERYAS_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    SKIP_FIELD_NUMBER: _ClassVar[int]
    TOP_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    orderby: str
    projection: str
    query: str
    queryas: str
    skip: int
    top: int
    def __init__(self, query: _Optional[str] = ..., collectionname: _Optional[str] = ..., projection: _Optional[str] = ..., top: _Optional[int] = ..., skip: _Optional[int] = ..., orderby: _Optional[str] = ..., queryas: _Optional[str] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ["results"]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: str
    def __init__(self, results: _Optional[str] = ...) -> None: ...

class UpdateDocumentRequest(_message.Message):
    __slots__ = ["collectionname", "document", "j", "query", "w"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    J_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    document: str
    j: bool
    query: str
    w: int
    def __init__(self, collectionname: _Optional[str] = ..., query: _Optional[str] = ..., document: _Optional[str] = ..., w: _Optional[int] = ..., j: bool = ...) -> None: ...

class UpdateDocumentResponse(_message.Message):
    __slots__ = ["opresult"]
    OPRESULT_FIELD_NUMBER: _ClassVar[int]
    opresult: UpdateResult
    def __init__(self, opresult: _Optional[_Union[UpdateResult, _Mapping]] = ...) -> None: ...

class UpdateOneRequest(_message.Message):
    __slots__ = ["collectionname", "item", "j", "w"]
    COLLECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    J_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    collectionname: str
    item: str
    j: bool
    w: int
    def __init__(self, collectionname: _Optional[str] = ..., item: _Optional[str] = ..., w: _Optional[int] = ..., j: bool = ...) -> None: ...

class UpdateOneResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class UpdateResult(_message.Message):
    __slots__ = ["acknowledged", "matchedCount", "modifiedCount", "upsertedCount", "upsertedId"]
    ACKNOWLEDGED_FIELD_NUMBER: _ClassVar[int]
    MATCHEDCOUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFIEDCOUNT_FIELD_NUMBER: _ClassVar[int]
    UPSERTEDCOUNT_FIELD_NUMBER: _ClassVar[int]
    UPSERTEDID_FIELD_NUMBER: _ClassVar[int]
    acknowledged: bool
    matchedCount: int
    modifiedCount: int
    upsertedCount: int
    upsertedId: str
    def __init__(self, acknowledged: bool = ..., matchedCount: _Optional[int] = ..., modifiedCount: _Optional[int] = ..., upsertedCount: _Optional[int] = ..., upsertedId: _Optional[str] = ...) -> None: ...
