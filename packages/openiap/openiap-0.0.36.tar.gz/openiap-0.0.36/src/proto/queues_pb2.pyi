from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateWorkflowInstanceRequest(_message.Message):
    __slots__ = ["data", "initialrun", "name", "resultqueue", "targetid", "workflowid"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    INITIALRUN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESULTQUEUE_FIELD_NUMBER: _ClassVar[int]
    TARGETID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOWID_FIELD_NUMBER: _ClassVar[int]
    data: str
    initialrun: bool
    name: str
    resultqueue: str
    targetid: str
    workflowid: str
    def __init__(self, targetid: _Optional[str] = ..., workflowid: _Optional[str] = ..., name: _Optional[str] = ..., resultqueue: _Optional[str] = ..., data: _Optional[str] = ..., initialrun: bool = ...) -> None: ...

class CreateWorkflowInstanceResponse(_message.Message):
    __slots__ = ["instanceid"]
    INSTANCEID_FIELD_NUMBER: _ClassVar[int]
    instanceid: str
    def __init__(self, instanceid: _Optional[str] = ...) -> None: ...

class QueueEvent(_message.Message):
    __slots__ = ["correlationId", "data", "exchangename", "queuename", "replyto", "routingkey"]
    CORRELATIONID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    EXCHANGENAME_FIELD_NUMBER: _ClassVar[int]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    REPLYTO_FIELD_NUMBER: _ClassVar[int]
    ROUTINGKEY_FIELD_NUMBER: _ClassVar[int]
    correlationId: str
    data: str
    exchangename: str
    queuename: str
    replyto: str
    routingkey: str
    def __init__(self, queuename: _Optional[str] = ..., correlationId: _Optional[str] = ..., replyto: _Optional[str] = ..., routingkey: _Optional[str] = ..., exchangename: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class QueueMessageRequest(_message.Message):
    __slots__ = ["correlationId", "data", "exchangename", "queuename", "replyto", "routingkey", "striptoken"]
    CORRELATIONID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    EXCHANGENAME_FIELD_NUMBER: _ClassVar[int]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    REPLYTO_FIELD_NUMBER: _ClassVar[int]
    ROUTINGKEY_FIELD_NUMBER: _ClassVar[int]
    STRIPTOKEN_FIELD_NUMBER: _ClassVar[int]
    correlationId: str
    data: str
    exchangename: str
    queuename: str
    replyto: str
    routingkey: str
    striptoken: bool
    def __init__(self, queuename: _Optional[str] = ..., correlationId: _Optional[str] = ..., replyto: _Optional[str] = ..., routingkey: _Optional[str] = ..., exchangename: _Optional[str] = ..., data: _Optional[str] = ..., striptoken: bool = ...) -> None: ...

class QueueMessageResponse(_message.Message):
    __slots__ = ["correlationId", "data", "exchangename", "queuename", "replyto", "routingkey"]
    CORRELATIONID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    EXCHANGENAME_FIELD_NUMBER: _ClassVar[int]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    REPLYTO_FIELD_NUMBER: _ClassVar[int]
    ROUTINGKEY_FIELD_NUMBER: _ClassVar[int]
    correlationId: str
    data: str
    exchangename: str
    queuename: str
    replyto: str
    routingkey: str
    def __init__(self, queuename: _Optional[str] = ..., correlationId: _Optional[str] = ..., replyto: _Optional[str] = ..., routingkey: _Optional[str] = ..., exchangename: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class RegisterExchangeRequest(_message.Message):
    __slots__ = ["addqueue", "algorithm", "exchangename", "routingkey"]
    ADDQUEUE_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    EXCHANGENAME_FIELD_NUMBER: _ClassVar[int]
    ROUTINGKEY_FIELD_NUMBER: _ClassVar[int]
    addqueue: bool
    algorithm: str
    exchangename: str
    routingkey: str
    def __init__(self, exchangename: _Optional[str] = ..., algorithm: _Optional[str] = ..., routingkey: _Optional[str] = ..., addqueue: bool = ...) -> None: ...

class RegisterExchangeResponse(_message.Message):
    __slots__ = ["queuename"]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    queuename: str
    def __init__(self, queuename: _Optional[str] = ...) -> None: ...

class RegisterQueueRequest(_message.Message):
    __slots__ = ["queuename"]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    queuename: str
    def __init__(self, queuename: _Optional[str] = ...) -> None: ...

class RegisterQueueResponse(_message.Message):
    __slots__ = ["queuename"]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    queuename: str
    def __init__(self, queuename: _Optional[str] = ...) -> None: ...

class UnRegisterQueueRequest(_message.Message):
    __slots__ = ["queuename"]
    QUEUENAME_FIELD_NUMBER: _ClassVar[int]
    queuename: str
    def __init__(self, queuename: _Optional[str] = ...) -> None: ...

class UnRegisterQueueResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
