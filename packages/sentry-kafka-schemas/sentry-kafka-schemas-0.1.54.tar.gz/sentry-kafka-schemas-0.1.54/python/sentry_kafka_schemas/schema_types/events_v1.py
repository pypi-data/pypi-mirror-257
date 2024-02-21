from typing import Dict, TypedDict, List, Tuple, Union, Any
from typing_extensions import Required


ErrorEvent = Union["_FourTrain", "_ThreeTrain"]
"""
error_event.

Aggregation type: anyOf
"""



class _Contexts(TypedDict, total=False):
    replay: "_ContextsReplay"
    """ Aggregation type: anyOf """

    trace: "_ContextsTrace"
    """ Aggregation type: anyOf """



_ContextsReplay = Union["_ReplayContext", None]
""" Aggregation type: anyOf """



_ContextsTrace = Union["_TraceContext", None]
""" Aggregation type: anyOf """



_ERROR_DATA_ERRORS_DEFAULT = None
""" Default value of the field path 'error data errors' """



_ERROR_DATA_HIERARCHICAL_HASHES_DEFAULT: List[Any] = []
""" Default value of the field path 'error data hierarchical_hashes' """



_ERROR_DATA_LOCATION_DEFAULT = None
""" Default value of the field path 'error data location' """



_ERROR_DATA_MODULES_DEFAULT = None
""" Default value of the field path 'error data modules' """



_ERROR_DATA_RECEIVED_DEFAULT = None
""" Default value of the field path 'error data received' """



_ERROR_DATA_VERSION_DEFAULT = None
""" Default value of the field path 'error data version' """



_ERROR_MESSAGE_PLATFORM_DEFAULT = None
""" Default value of the field path 'error message platform' """



_ERROR_MESSAGE_RETENTION_DAYS_DEFAULT = None
""" Default value of the field path 'error message retention_days' """



class _ErrorData(TypedDict, total=False):
    contexts: "_ErrorDataContexts"
    """ Aggregation type: anyOf """

    culprit: Any
    errors: Union[List[Any], None]
    """
    default: None
    items: True
    """

    exception: "_ErrorDataException"
    """ Aggregation type: anyOf """

    hierarchical_hashes: List[str]
    """
    default:
      []
    """

    location: Union[str, None]
    """ default: None """

    modules: Union[Dict[str, Union[str, None]], None]
    """
    default: None
    additionalProperties:
      type:
      - string
      - 'null'
    """

    received: Union[Union[int, float], None]
    """ default: None """

    request: "_ErrorDataRequest"
    """ Aggregation type: anyOf """

    sdk: "_ErrorDataSdk"
    """ Aggregation type: anyOf """

    tags: Union[List["_ErrorDataTagsArrayItem"], None]
    """
    items:
      items:
      - $ref: '#/definitions/Unicodify'
        used: !!set
          $ref: null
      - $ref: '#/definitions/Unicodify'
        used: !!set
          $ref: null
      maxItems: 2
      minItems: 2
      type:
      - array
      - 'null'
    """

    threads: "_ErrorDataThreads"
    """ Aggregation type: anyOf """

    title: Any
    type: Any
    user: "_ErrorDataUser"
    """ Aggregation type: anyOf """

    version: Union[str, None]
    """ default: None """



_ErrorDataContexts = Union["_Contexts", None]
""" Aggregation type: anyOf """



_ErrorDataException = Union["_Exception", None]
""" Aggregation type: anyOf """



_ErrorDataRequest = Union["_Request", None]
""" Aggregation type: anyOf """



_ErrorDataSdk = Union["_Sdk", None]
""" Aggregation type: anyOf """



_ErrorDataTagsArrayItem = Union[Tuple[Any, Any], None]
"""
items:
  - $ref: '#/definitions/Unicodify'
    used: !!set
      $ref: null
  - $ref: '#/definitions/Unicodify'
    used: !!set
      $ref: null
maxItems: 2
minItems: 2
"""



_ErrorDataThreads = Union["_Thread", None]
""" Aggregation type: anyOf """



_ErrorDataUser = Union["_User", None]
""" Aggregation type: anyOf """



class _ErrorMessage(TypedDict, total=False):
    data: Required["_ErrorData"]
    """ Required property """

    datetime: str
    event_id: Required[str]
    """ Required property """

    group_id: Required[int]
    """
    minimum: 0

    Required property
    """

    message: Required[str]
    """ Required property """

    platform: Union[str, None]
    """ default: None """

    primary_hash: Required[str]
    """ Required property """

    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    retention_days: Union[int, None]
    """
    default: None
    minimum: 0
    """



class _Exception(TypedDict, total=False):
    values: Union[List["_ExceptionValuesArrayItem"], None]
    """
    items:
      anyOf:
      - $ref: '#/definitions/ExceptionValue'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null
    """



class _ExceptionMechanism(TypedDict, total=False):
    handled: Any
    type: Any


class _ExceptionValue(TypedDict, total=False):
    mechanism: "_ExceptionValueMechanism"
    """ Aggregation type: anyOf """

    stacktrace: "_ExceptionValueStacktrace"
    """ Aggregation type: anyOf """

    thread_id: "_ExceptionValueThreadId"
    """ Aggregation type: anyOf """

    type: Any
    value: Any


_ExceptionValueMechanism = Union["_ExceptionMechanism", None]
""" Aggregation type: anyOf """



_ExceptionValueStacktrace = Union["_StackTrace", None]
""" Aggregation type: anyOf """



_ExceptionValueThreadId = Union["_ThreadId", None]
""" Aggregation type: anyOf """



_ExceptionValuesArrayItem = Union["_ExceptionValue", None]
""" Aggregation type: anyOf """



_FourTrain = Tuple["_FourTrain0", str, "_ErrorMessage", Any]
"""
maxItems: 4
minItems: 4
"""



_FourTrain0 = int
""" minimum: 0 """



class _ReplacementEvent(TypedDict, total=False):
    project_id: Required[int]
    """
    minimum: 0

    Required property
    """



class _ReplayContext(TypedDict, total=False):
    replay_id: Union[str, None]


class _Request(TypedDict, total=False):
    headers: Union[List["_RequestHeadersArrayItem"], None]
    """
    items:
      items:
      - type: string
      - $ref: '#/definitions/Unicodify'
        used: !!set
          $ref: null
      maxItems: 2
      minItems: 2
      type:
      - array
      - 'null'
    """

    method: Any


_RequestHeadersArrayItem = Union[Tuple[str, Any], None]
"""
items:
  - type: string
  - $ref: '#/definitions/Unicodify'
    used: !!set
      $ref: null
maxItems: 2
minItems: 2
"""



_STACK_FRAME_COLNO_DEFAULT = None
""" Default value of the field path 'stack frame colno' """



_STACK_FRAME_IN_APP_DEFAULT = None
""" Default value of the field path 'stack frame in_app' """



_STACK_FRAME_LINENO_DEFAULT = None
""" Default value of the field path 'stack frame lineno' """



class _Sdk(TypedDict, total=False):
    integrations: Union[List[Any], None]
    """
    items:
      $ref: '#/definitions/Unicodify'
      used: !!set
        $ref: null
    """

    name: Any
    version: Any


class _StackFrame(TypedDict, total=False):
    abs_path: Any
    colno: Union[int, None]
    """
    default: None
    minimum: 0
    """

    filename: Any
    function: Any
    in_app: Union[bool, None]
    """ default: None """

    lineno: Union[int, None]
    """
    default: None
    minimum: 0
    """

    module: Any
    package: Any


class _StackTrace(TypedDict, total=False):
    frames: Union[List["_StackTraceFramesArrayItem"], None]
    """
    items:
      anyOf:
      - $ref: '#/definitions/StackFrame'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null
    """



_StackTraceFramesArrayItem = Union["_StackFrame", None]
""" Aggregation type: anyOf """



_THREAD_VALUE_MAIN_DEFAULT = None
""" Default value of the field path 'thread value main' """



_TRACE_CONTEXT_SAMPLED_DEFAULT = None
""" Default value of the field path 'trace context sampled' """



_TRACE_CONTEXT_SPAN_ID_DEFAULT = None
""" Default value of the field path 'trace context span_id' """



_TRACE_CONTEXT_TRACE_ID_DEFAULT = None
""" Default value of the field path 'trace context trace_id' """



class _Thread(TypedDict, total=False):
    values: Union[List["_ThreadValuesArrayItem"], None]
    """
    items:
      anyOf:
      - $ref: '#/definitions/ThreadValue'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null
    """



_ThreadId = Union["_ThreadIdAnyof0", str]
""" Aggregation type: anyOf """



_ThreadIdAnyof0 = int
""" minimum: 0 """



class _ThreadValue(TypedDict, total=False):
    id: "_ThreadValueId"
    """ Aggregation type: anyOf """

    main: Union[bool, None]
    """ default: None """



_ThreadValueId = Union["_ThreadId", None]
""" Aggregation type: anyOf """



_ThreadValuesArrayItem = Union["_ThreadValue", None]
""" Aggregation type: anyOf """



_ThreeTrain = Tuple["_ThreeTrain0", str, "_ReplacementEvent"]
"""
maxItems: 3
minItems: 3
"""



_ThreeTrain0 = int
""" minimum: 0 """



class _TraceContext(TypedDict, total=False):
    sampled: Union[bool, None]
    """ default: None """

    span_id: Union[str, None]
    """ default: None """

    trace_id: Union[str, None]
    """ default: None """



_USER_IP_ADDRESS_DEFAULT = None
""" Default value of the field path 'user ip_address' """



class _User(TypedDict, total=False):
    email: Any
    geo: Union[Dict[str, Any], None]
    """
    additionalProperties:
      $ref: '#/definitions/ContextStringify'
      used: !!set
        $ref: null
    """

    id: Any
    ip_address: Union[str, None]
    """ default: None """

    username: Any
