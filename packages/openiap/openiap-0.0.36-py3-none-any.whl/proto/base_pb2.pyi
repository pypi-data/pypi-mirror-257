from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import any_pb2 as _any_pb2
import querys_pb2 as _querys_pb2
import queues_pb2 as _queues_pb2
import watch_pb2 as _watch_pb2
import workitems_pb2 as _workitems_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BeginStream(_message.Message):
    __slots__ = ["checksum", "stat"]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    STAT_FIELD_NUMBER: _ClassVar[int]
    checksum: str
    stat: Stat
    def __init__(self, checksum: _Optional[str] = ..., stat: _Optional[_Union[Stat, _Mapping]] = ...) -> None: ...

class CustomCommandRequest(_message.Message):
    __slots__ = ["command", "data", "id", "name"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    command: str
    data: str
    id: str
    name: str
    def __init__(self, command: _Optional[str] = ..., id: _Optional[str] = ..., name: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class CustomCommandResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class DownloadRequest(_message.Message):
    __slots__ = ["filename", "id"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    filename: str
    id: str
    def __init__(self, id: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class DownloadResponse(_message.Message):
    __slots__ = ["filename", "id", "mimetype"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MIMETYPE_FIELD_NUMBER: _ClassVar[int]
    filename: str
    id: str
    mimetype: str
    def __init__(self, id: _Optional[str] = ..., filename: _Optional[str] = ..., mimetype: _Optional[str] = ...) -> None: ...

class EndStream(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Envelope(_message.Message):
    __slots__ = ["command", "data", "id", "jwt", "priority", "rid", "seq", "spanid", "traceid"]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    RID_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    SPANID_FIELD_NUMBER: _ClassVar[int]
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    command: str
    data: _any_pb2.Any
    id: str
    jwt: str
    priority: int
    rid: str
    seq: int
    spanid: str
    traceid: str
    def __init__(self, command: _Optional[str] = ..., priority: _Optional[int] = ..., seq: _Optional[int] = ..., id: _Optional[str] = ..., rid: _Optional[str] = ..., data: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., jwt: _Optional[str] = ..., traceid: _Optional[str] = ..., spanid: _Optional[str] = ...) -> None: ...

class ErrorResponse(_message.Message):
    __slots__ = ["code", "message", "stack"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STACK_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    stack: str
    def __init__(self, message: _Optional[str] = ..., code: _Optional[int] = ..., stack: _Optional[str] = ...) -> None: ...

class GetElementRequest(_message.Message):
    __slots__ = ["xpath"]
    XPATH_FIELD_NUMBER: _ClassVar[int]
    xpath: str
    def __init__(self, xpath: _Optional[str] = ...) -> None: ...

class GetElementResponse(_message.Message):
    __slots__ = ["xpath"]
    XPATH_FIELD_NUMBER: _ClassVar[int]
    xpath: str
    def __init__(self, xpath: _Optional[str] = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PingResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RefreshToken(_message.Message):
    __slots__ = ["jwt", "user", "username"]
    JWT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    jwt: str
    user: User
    username: str
    def __init__(self, username: _Optional[str] = ..., jwt: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class Role(_message.Message):
    __slots__ = ["_id", "name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    _ID_FIELD_NUMBER: _ClassVar[int]
    _id: str
    name: str
    def __init__(self, _id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class SigninRequest(_message.Message):
    __slots__ = ["agent", "jwt", "longtoken", "password", "ping", "username", "validateonly", "version"]
    AGENT_FIELD_NUMBER: _ClassVar[int]
    JWT_FIELD_NUMBER: _ClassVar[int]
    LONGTOKEN_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    VALIDATEONLY_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    agent: str
    jwt: str
    longtoken: bool
    password: str
    ping: bool
    username: str
    validateonly: bool
    version: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., jwt: _Optional[str] = ..., ping: bool = ..., validateonly: bool = ..., agent: _Optional[str] = ..., version: _Optional[str] = ..., longtoken: bool = ...) -> None: ...

class SigninResponse(_message.Message):
    __slots__ = ["jwt", "user"]
    JWT_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    jwt: str
    user: User
    def __init__(self, jwt: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class Stat(_message.Message):
    __slots__ = ["birthtimeMs", "blksize", "blocks", "ctime", "ctimeMs", "dev", "gid", "ino", "mode", "mtime", "mtimeMs", "nlink", "rdev", "size", "uid"]
    BIRTHTIMEMS_FIELD_NUMBER: _ClassVar[int]
    BLKSIZE_FIELD_NUMBER: _ClassVar[int]
    BLOCKS_FIELD_NUMBER: _ClassVar[int]
    CTIMEMS_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    DEV_FIELD_NUMBER: _ClassVar[int]
    GID_FIELD_NUMBER: _ClassVar[int]
    INO_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    MTIMEMS_FIELD_NUMBER: _ClassVar[int]
    MTIME_FIELD_NUMBER: _ClassVar[int]
    NLINK_FIELD_NUMBER: _ClassVar[int]
    RDEV_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    birthtimeMs: float
    blksize: int
    blocks: int
    ctime: _timestamp_pb2.Timestamp
    ctimeMs: float
    dev: int
    gid: int
    ino: int
    mode: int
    mtime: _timestamp_pb2.Timestamp
    mtimeMs: float
    nlink: int
    rdev: int
    size: int
    uid: int
    def __init__(self, birthtimeMs: _Optional[float] = ..., blksize: _Optional[int] = ..., blocks: _Optional[int] = ..., ctime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., ctimeMs: _Optional[float] = ..., dev: _Optional[int] = ..., gid: _Optional[int] = ..., ino: _Optional[int] = ..., mode: _Optional[int] = ..., mtime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., mtimeMs: _Optional[float] = ..., nlink: _Optional[int] = ..., rdev: _Optional[int] = ..., size: _Optional[int] = ..., uid: _Optional[int] = ...) -> None: ...

class Stream(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class UploadRequest(_message.Message):
    __slots__ = ["filename", "mimetype"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    MIMETYPE_FIELD_NUMBER: _ClassVar[int]
    filename: str
    mimetype: str
    def __init__(self, filename: _Optional[str] = ..., mimetype: _Optional[str] = ...) -> None: ...

class UploadResponse(_message.Message):
    __slots__ = ["bytes", "chunks", "elapsedTime", "filename", "id", "mb", "mbps"]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    ELAPSEDTIME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MBPS_FIELD_NUMBER: _ClassVar[int]
    MB_FIELD_NUMBER: _ClassVar[int]
    bytes: int
    chunks: int
    elapsedTime: int
    filename: str
    id: str
    mb: float
    mbps: float
    def __init__(self, id: _Optional[str] = ..., filename: _Optional[str] = ..., bytes: _Optional[int] = ..., chunks: _Optional[int] = ..., mb: _Optional[float] = ..., elapsedTime: _Optional[int] = ..., mbps: _Optional[float] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["_id", "email", "name", "roles", "username"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    _ID_FIELD_NUMBER: _ClassVar[int]
    _id: str
    email: str
    name: str
    roles: _containers.RepeatedCompositeFieldContainer[Role]
    username: str
    def __init__(self, _id: _Optional[str] = ..., name: _Optional[str] = ..., username: _Optional[str] = ..., email: _Optional[str] = ..., roles: _Optional[_Iterable[_Union[Role, _Mapping]]] = ...) -> None: ...
